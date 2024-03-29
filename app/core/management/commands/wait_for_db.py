"""
Django command to wait for the database to be available
"""
import time
from django.db import connections
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
                # from django.db import connection
                # connection.ensure_connection()
                # db_up = True

                # self.check(databases=['default'])
                connections['default'].ensure_connection()
                # self.check() #old code
                # connection.ensure_connection() #new changes
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
            # time.sleep(10)
        self.stdout.write(self.style.SUCCESS('Database available'))