import sqlite3
from pathlib import Path

from utils.extract import extract_records

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

from django.core.management.base import BaseCommand, CommandError
from budget.models import *


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


