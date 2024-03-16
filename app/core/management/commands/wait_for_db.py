"""
Django command to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
# from django.db import connection #new changes


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Enrytpoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                # self.check() #old code
                # connection.ensure_connection() #new changes

                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
            # time.sleep(10)
        self.stdout.write(self.style.SUCCESS('Database available'))