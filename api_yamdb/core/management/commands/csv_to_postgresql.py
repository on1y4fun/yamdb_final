import csv
from django.core.management.base import BaseCommand
import psycopg2
import secrets
import string

from api_yamdb.settings import COMMAND_CHOICES, DATABASES
from users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--import',
            default=False,
            nargs='?',
            choices=COMMAND_CHOICES.keys(),
            help='import data from csv'
        )

    def handle(self, *args, **options):
        data_path = f'static/data/{options["import"]}.csv'
        with open(data_path, 'r', encoding='utf8') as csv_file:
            database = csv.DictReader(csv_file)
            connection = psycopg2.connect(
                dbname=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD'],
                host=DATABASES['default']['HOST'],
                port=DATABASES['default']['PORT'],
            )

            if options['import'] == 'users':
                chars = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(chars) for char in range(8))
                for row in database:
                    User.objects.create_user(
                        pk=row['id'],
                        username=row['username'],
                        password=password,
                        email=row['email'],
                    )

            cursor = connection.cursor()
            columns = ','.join(database.fieldnames)
            sql_request = f"""copy
                        {COMMAND_CHOICES[options['import']]}({columns})
                        from stdout with (format csv)"""
            cursor.copy_expert(sql_request, csv_file)
            connection.commit()
