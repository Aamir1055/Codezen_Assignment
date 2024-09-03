from celery import shared_task
import pandas as pd
from django.conf import settings
from .models import Product
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@shared_task
def test_task():
    file_path = Path(settings.BASE_DIR) / 'store' / 'management' / 'commands' / 'command_data' / 'products.xlsx'
    try:
        data = pd.read_excel(file_path)
        for _, row in data.iterrows():
            name = row['product_name']
            amount = row['amount']
            if not Product.objects.filter(name=name).exists():
                Product.objects.create(name=name, amount=amount)
    except Exception as e:
        logger.error(f"Error: {e}")
