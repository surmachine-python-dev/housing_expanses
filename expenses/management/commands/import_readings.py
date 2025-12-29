import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import MeterReading
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Import readings from sample.xlsx'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('planing', 'sample.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading excel: {e}'))
            return

        # Create users
        user_michal, _ = User.objects.get_or_create(username='Michał')
        user_ania, _ = User.objects.get_or_create(username='Ania')

        count = 0

        for index, row in df.iterrows():
            date_val = row['Data:']
            if pd.isnull(date_val):
                continue
            
            # Ensure date is a date object
            if isinstance(date_val, datetime):
                # Normalize to 1st of the month
                date = date_val.date().replace(day=1)
            else:
                # Try to parse if string, or skip
                try:
                    # Normalize to 1st of the month
                    date = pd.to_datetime(date_val).date().replace(day=1)
                except:
                    continue


            # Michał User Readings
            readings_michal = [
                ('Cold Water', row.get('Woda zimna:')),
                ('Hot Water', row.get('Woda ciepła:')),
                ('Energy', row.get('Prąd:')),
                ('Heating', row.get('Ogrzewanie:')),
            ]

            for utility, value in readings_michal:
                if pd.notnull(value):
                    MeterReading.objects.get_or_create(
                        user=user_michal,

                        date=date,
                        utility_type=utility,
                        defaults={'reading_value': value}
                    )
                    count += 1

            # Ania User Readings
            readings_ania = [
                ('Cold Water', row.get('Woda zimna:.1')),
                ('Hot Water', row.get('Woda ciepła:.1')),
                ('Heating', row.get('Ogrzewanie:.1')),
            ]

            for utility, value in readings_ania:
                if pd.notnull(value):
                    MeterReading.objects.get_or_create(
                        user=user_ania,
                        date=date,
                        utility_type=utility,
                        defaults={'reading_value': value}
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} readings'))
