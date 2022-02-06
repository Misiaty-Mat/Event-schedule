from django.core.management.base import BaseCommand

from core.models import Event

from datetime import datetime, timedelta

class Command(BaseCommand):
    """Auto delete rows in Event database that is 30 days after the deadline"""
    
    def handle(self, *args, **kwargs):
        Event.objects.filter(event_date__lte=datetime.now()-timedelta(days=30)).delete()
        self.stdout.write('Deleting Event rows 30 days past the deadline...')
        