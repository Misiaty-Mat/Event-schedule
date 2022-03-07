from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from core.models import Event
from .test_models import sample_user

from datetime import date, timedelta


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

    def test_delete_old_events(self):
        """Test command for deleting Event rows 30 days past the deadline"""
        Event.objects.create(
            title="Future Event",
            user=sample_user('Mati', 'test@email.com'),
            event_date=date.today()
        )
        Event.objects.create(
            title="Event past the deadline",
            user=sample_user('Eddie', 'test2@email.com'),
            event_date=date.today() - timedelta(31)
        )
        call_command('delete_old_events')
        event_len = Event.objects.all().count()
        self.assertEqual(event_len, 1)
