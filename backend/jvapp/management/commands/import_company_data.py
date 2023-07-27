import numpy as np
import pandas as pd
from django.core.management import BaseCommand

from jvapp.models.external import ExternalCompanyData
from jvapp.utils.data import coerce_int

RECORD_SAVE_CHUNK_SIZE = 5000


class Command(BaseCommand):
    help = 'Import company data from chunked CSV files'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--file_idx_start',
            type=int,
            help='The start index for file processing',
        )
        parser.add_argument(
            '--file_idx_end',
            type=int,
            help='The end index for file processing',
        )
    
    def handle(self, *args, **options):
        file_idx_start = options['file_idx_start'] or 1
        file_idx_end = options['file_idx_end'] or 32
        for file_idx in range(file_idx_start, file_idx_end + 1):
            self.stdout.write(f'Reading records from file IDX = {file_idx} of company data')
            data_frame = pd.read_csv(
                f'https://jobvyne.nyc3.digitaloceanspaces.com/media/large_datasets/companies-dataset-2023-02_{file_idx}.csv',
                engine='python'
            )
            data_frame.replace({np.nan: None}, inplace=True)
            companies = []
            for idx, (_, row) in enumerate(data_frame.iterrows()):
                # skip header
                if idx == 0:
                    continue
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
                if len(companies) == 1:
                    self.stdout.write(f'First company in batch is {row["name"]}')
                if len(companies) == RECORD_SAVE_CHUNK_SIZE:
                    ExternalCompanyData.objects.bulk_create(companies, ignore_conflicts=True)
                    self.stdout.write(f'Saved {RECORD_SAVE_CHUNK_SIZE} companies')
                    companies = []
            if companies:
                ExternalCompanyData.objects.bulk_create(companies, ignore_conflicts=True)
                self.stdout.write(f'Saved {len(companies)} companies')
        self.stdout.write(self.style.SUCCESS('Completed importing company data!'))
