import sqlite3
from pathlib import Path

from budget.models import BankAccount, IncomeSubCategory, IncomeCategory, ExpenditureSubCategory, ExpenditureCategory
from utils.extract import extract_records

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "заполняет БД из заранее сохраненной копии"

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--dbfile',
            help='имя файла базы данных'
        )

    def handle(self, *args, **options):
        dbfile = BASE_DIR / options['dbfile']
        # Create a SQL connection to our SQLite database
        con = sqlite3.connect(dbfile)
        self.stdout.write(self.style.SUCCESS('успешно открыт файл базы данных "%s"' % dbfile))

        accounts = extract_records(
            con,
            "select _id as id, name, initial_funds as incoming_balance, "
            "not(use_account - 1) as is_active, creation_time_ms "
            "from account"
        )
        BankAccount.objects_with_deleted.delete(hard=True)
        BankAccount.objects.bulk_create(
            [
                BankAccount(
                    id=account.id,
                    name=account.name,
                    incoming_balance=account.incoming_balance,
                    is_active=account.is_active,
                ) for account in accounts
            ]
        )
        self.stdout.write(self.style.SUCCESS('успешно загружены банковские счета'))

        categories = extract_records(
            con,
            "select _id as id, name, parent_id, ei "
            "from categories_table order by parent_id"
        )
        IncomeSubCategory.objects_with_deleted.delete(hard=True)
        IncomeCategory.objects_with_deleted.delete(hard=True)
        ExpenditureSubCategory.objects_with_deleted.delete(hard=True)
        ExpenditureCategory.objects_with_deleted.delete(hard=True)
        for category in categories:
            Category_ = ExpenditureCategory if category.ei == 0 else IncomeCategory
            SubCategory_ = ExpenditureSubCategory if category.ei == 0 else IncomeSubCategory
            if category.parent_id == 0:
                category_, _ = Category_.objects.update_or_create(
                    id=category.id,
                    name=category.name
                )
            else:
                SubCategory_.objects.create(
                    id=category.id,
                    name=category.name,
                    category=Category_.objects.get(id=category.parent_id)
                )
        self.stdout.write(self.style.SUCCESS('успешно загружены категории'))
        con.close()


