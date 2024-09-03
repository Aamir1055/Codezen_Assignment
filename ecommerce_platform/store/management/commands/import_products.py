import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from store.models import Product

class Command(BaseCommand):
    help = 'Import products from an Excel file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\Aamir\Desktop\codezen_assignment\ecommerce_platform\store\management\commands\command_data\product_data.xlsx'
        
        if not os.path.exists(file_path):
            raise CommandError('Excel file not found.')
        
        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file_path)
            
            # Iterate over the rows in the DataFrame and create Product instances
            for index, row in df.iterrows():
                product_name = row['product_name']
                product_amount = row['amount']
                
                # Check for duplicate entries
                if not Product.objects.filter(name=product_name).exists():
                    Product.objects.create(name=product_name, amount=product_amount)
                else:
                    self.stdout.write(self.style.WARNING(f"Product '{product_name}' already exists and will not be duplicated."))

            self.stdout.write(self.style.SUCCESS('Successfully imported products from Excel file'))
        except Exception as e:
            raise CommandError(f'Error reading Excel file: {str(e)}')
