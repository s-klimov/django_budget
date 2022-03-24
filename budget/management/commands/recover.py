import os.path
import sqlite3
from datetime import datetime
from pathlib import Path

from budget.models import BankAccount, IncomeSubCategory, IncomeCategory, ExpenditureSubCategory, ExpenditureCategory, \
    Expenditure, Income, Transfer
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
        dbfile = os.path.join(BASE_DIR, options['dbfile'])

        Expenditure.objects_with_deleted.delete(hard=True)
        Income.objects_with_deleted.delete(hard=True)
        Transfer.objects_with_deleted.delete(hard=True)
        IncomeSubCategory.objects_with_deleted.delete(hard=True)
        IncomeCategory.objects_with_deleted.delete(hard=True)
        ExpenditureSubCategory.objects_with_deleted.delete(hard=True)
        ExpenditureCategory.objects_with_deleted.delete(hard=True)
        BankAccount.objects_with_deleted.delete(hard=True)

        # Create a SQL connection to our SQLite database
        con = sqlite3.connect(dbfile)
        self.stdout.write(self.style.SUCCESS('успешно открыт файл базы данных "%s"' % dbfile))

        accounts = extract_records(
            con,
            "select _id as id, name, initial_funds as incoming_balance, "
            "not(use_account - 1) as is_active "
            "from account"
        )
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
                    category_id=category.parent_id
                )
        ExpenditureSubCategory.objects.create(name="Питание", category_id=4)
        ExpenditureSubCategory.objects.create(name="Покупка товаров", category_id=4)
        IncomeSubCategory.objects.create(name="Другое (Доходы)", category_id=2)
        self.stdout.write(self.style.SUCCESS('успешно загружены категории'))

        expenditures = extract_records(
            con,
            "select value, category, account, date "
            "from income_or_expense where i_e=0 and from_or_to is null"
        )
        Expenditure.objects.bulk_create(
            [
                Expenditure(
                    value=expenditure.value,
                    bank_account=BankAccount.objects.get(name=expenditure.account),
                    sub_category=ExpenditureSubCategory.objects.get(name=expenditure.category),
                    operation_date=datetime.utcfromtimestamp(expenditure.date/1000)
                ) for expenditure in expenditures
            ]
        )
        self.stdout.write(self.style.SUCCESS('успешно загружены расходы'))

        incomes = extract_records(
            con,
            "select value, category, account, date "
            "from income_or_expense where i_e=1 and from_or_to is null"
        )
        Income.objects.bulk_create(
            [
                Income(
                    value=income.value,
                    bank_account=BankAccount.objects.get(name=income.account),
                    sub_category=IncomeSubCategory.objects.get(name=income.category),
                    operation_date=datetime.utcfromtimestamp(income.date/1000)
                ) for income in incomes
            ]
        )
        self.stdout.write(self.style.SUCCESS('успешно загружены доходы'))

        con.close()


