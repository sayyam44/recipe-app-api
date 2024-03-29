# """
# Test custom Django management commands.
# """
# from unittest.mock import patch

# from psycopg2 import OperationalError as Psycopg2Error

# from django.core.management import call_command
# from django.db.utils import OperationalError
# from django.test import SimpleTestCase

# #below is the command that we will be mocking
# @patch('core.management.commands.wait_for_db.Command.check')
# class CommandTests(SimpleTestCase):
#     """ Test commands."""

#     def test_wait_for_db_ready(self, pathed_check):
#         """Test waititng for databse if database ready."""
#         pathed_check.return_value = True

#         call_command('wait_for_db')
#         # patched_check.assert_called_once_with() #new code
#         pathed_check.assert_called_once_with(databases=['default']) #old 
#         # patched_check.assert_called_once_with()


#     @patch('time.sleep')
#     def test_wait_for_db_delay(self, patched_sleep, patched_check):
#         """Test waiting for database when getting OperationalError."""
#         patched_check.side_effect = [Psycopg2Error] * 2 + \
#             [OperationalError] * 3 + [True]

#         call_command('wait_for_db')

#         self.assertEqual(patched_check.call_count, 6)
#         # patched_check.assert_called_with() #new code
#         patched_check.assert_called_with(databases=['default']) #old code

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
