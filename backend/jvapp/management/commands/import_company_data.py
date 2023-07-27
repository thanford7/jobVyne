import numpy as np
import pandas as pd
from django.core.management import BaseCommand

from jvapp.models.external import ExternalCompanyData
from jvapp.utils.data import coerce_int

ROW_DOWNLOAD_CHUNK_SIZE = 500000
RECORD_SAVE_CHUNK_SIZE = 5000


class Command(BaseCommand):
    help = 'Import company data from CSV file'

    def handle(self, *args, **options):
        current_row_idx = ExternalCompanyData.objects.count() + 1
        file_url = 'https://jobvyne.nyc3.digitaloceanspaces.com/media/large_datasets/companies-dataset-2023-02.csv'
        while True:
            self.stdout.write(f'Reading lines {current_row_idx} to {current_row_idx + ROW_DOWNLOAD_CHUNK_SIZE} of company data')
            data_frame = pd.read_csv(
                file_url, skiprows=current_row_idx, nrows=ROW_DOWNLOAD_CHUNK_SIZE, engine='python',
                names=[
                    'handle', 'type', 'name', 'website', 'founded', 'industry', 'size', 'city', 'state', 'country_code'
                ], dtype={
                    'handle': np.object,
                    'type': np.object,
                    'name': np.object,
                    'website': np.object,
                    'founded': np.object,
                    'industry': np.object,
                    'size': np.object,
                    'city': np.object,
                    'state': np.object,
                    'country_code': np.object,
                }
            )
            if data_frame.empty:
                break
            data_frame.replace({np.nan: None}, inplace=True)
            companies = []
            for idx, row in data_frame.iterrows():
                if not all((row['name'], row['website'])):
                    continue
                size_min = None
                size_max = None
                if row['size'] and '-' in str(row['size']):
                    size_min, size_max = row['size'].split('-')
                companies.append(ExternalCompanyData(
                    company_name=row['name'],
                    linkedin_handle=row['handle'],
                    website=row['website'],
                    industry=row['industry'],
                    size_min=coerce_int(size_min),
                    size_max=coerce_int(size_max),
                    company_type=row['type'],
                    founded_year=coerce_int(row['founded']),
                    city=row['city'],
                    state=row['state'],
                    country_code=row['country_code']
                ))
                if len(companies) == RECORD_SAVE_CHUNK_SIZE:
                    ExternalCompanyData.objects.bulk_create(companies, ignore_conflicts=True)
                    self.stdout.write(f'Saved {RECORD_SAVE_CHUNK_SIZE} companies')
                    companies = []
            if companies:
                ExternalCompanyData.objects.bulk_create(companies, ignore_conflicts=True)
                self.stdout.write(f'Saved {len(companies)} companies')
            current_row_idx += ROW_DOWNLOAD_CHUNK_SIZE
        self.stdout.write(self.style.SUCCESS('Completed importing company data!'))
