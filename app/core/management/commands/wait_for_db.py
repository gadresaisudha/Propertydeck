"""
Django command to wait for database to be available
"""

from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('waiting for database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting for 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
