from django.core.management.base import BaseCommand
from stock.models import Stock
import json

class Command(BaseCommand):
    help = 'import stocks json file'

    def add_arguments(self, parser):
        pass

    
    def handle(self, *args, **options):
        with open('instruments_data.json') as f:
            data = json.load(f)
            for stock in data:
                models = Stock(name=stock['name'], symbol=stock['symbol'])
                models.save()
        
