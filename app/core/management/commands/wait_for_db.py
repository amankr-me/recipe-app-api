"""
Django commands to wait for dataase to be available
"""

import time

from psycopg2 import OperationalError as psycopg2OpError

from django.db.utils import OperationalError

from typing import Any, Optional  # noqa
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db"""
    def handle(self, *args, **options):
        """Entry point for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2OpError, OperationalError):
                self.stdout.write("Database Unavailable, waiting 1 sec ...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
