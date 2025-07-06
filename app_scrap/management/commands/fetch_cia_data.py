import requests
import hashlib
import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from bs4 import BeautifulSoup
from app_scrap.models import DataPull, CIAData, DataChange







def parse_cia_data():
    base_url = "https://oig.hhs.gov/compliance/corporate-integrity-agreements/cia-documents.asp#"
    all_data = []
    
    # Letters to process (A-Z)
    letters = [chr(i) for i in range(97, 123)]  # a to z
    
    my_var = 0
    for letter in letters:
        url = f"{base_url}{letter}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cia_table = soup.find('table', {'id': 'cia_list'})
        
        if not cia_table:
            continue
            
        # Process table rows
        for row in cia_table.find_all('tr'):
            # Skip header rows (those with <th> elements) and empty rows
            if row.find('th') or not row.find('td'):
                continue
                
            columns = row.find_all('td')
            if len(columns) < 5:  # Ensure we have all 5 columns
                continue
                
            # if my_var < 3: 
            #     provider = columns[0].get_text(strip=True)+"002"
            #     city = columns[1].get_text(strip=True)
            #     state = columns[2].get_text(strip=True)
            #     effective = columns[3].get_text(strip=True)
            # else: 
            provider = columns[0].get_text(strip=True)
            city = columns[1].get_text(strip=True)
            state = columns[2].get_text(strip=True)
            effective = columns[3].get_text(strip=True)
            
            my_var += 1
            
            # Handle press release link
            press_release_elem = columns[4].find('a')
            press_release = press_release_elem['href'] if press_release_elem else None
            
            all_data.append({
                'provider': provider,
                'city': city,
                'state': state,
                'effective': effective,
                'press_release': press_release
            })
    
    return all_data


def generate_record_hash(record):
    """Generate SHA-256 hash for record comparison"""
    # Create a stable string representation of the record
    data_str = f"{record['provider']}|{record['city']}|{record['state']}|{record['effective']}|{record['press_release']}"
    return hashlib.sha256(data_str.encode()).hexdigest()


class Command(BaseCommand):
    help = 'Fetches and processes CIA data'
    
    def handle(self, *args, **options):
        self.stdout.write("Starting CIA data fetch...")
        
        # Create new data pull
        current_pull = DataPull.objects.create()
        self.stdout.write(f"Created new DataPull ID: {current_pull.id}")
        
        # Fetch and process data
        current_data = parse_cia_data()
        self.stdout.write(f"Fetched {len(current_data)} records")
        
        current_hashes = set()
        
        # Store current data
        for record in current_data:
            record_hash = generate_record_hash(record)
            current_hashes.add(record_hash)
            
            CIAData.objects.create(
                data_pull=current_pull,
                record_hash=record_hash,
                **record
            )
        
        # Compare with previous pull
        previous_pull = DataPull.objects.filter(is_processed=True).order_by('-pull_time').first()
        change_count = 0
        
        if previous_pull:
            self.stdout.write(f"Comparing with previous pull ID: {previous_pull.id}")
            previous_records = CIAData.objects.filter(data_pull=previous_pull)
            previous_hashes = {r.record_hash for r in previous_records}
            
            # Find added records
            added_hashes = current_hashes - previous_hashes
            if added_hashes:
                self.stdout.write(f"Found {len(added_hashes)} added records")
                
            for record in current_data:
                record_hash = generate_record_hash(record)
                if record_hash in added_hashes:
                    DataChange.objects.create(
                        data_pull=current_pull,
                        change_type='added',
                        provider=record['provider'],
                        current_data=record
                    )
                    change_count += 1
            
            # Find removed records
            removed_hashes = previous_hashes - current_hashes
            if removed_hashes:
                self.stdout.write(f"Found {len(removed_hashes)} removed records")
                
            for record in previous_records:
                if record.record_hash in removed_hashes:
                    DataChange.objects.create(
                        data_pull=current_pull,
                        change_type='removed',
                        provider=record.provider,
                        previous_data={
                            'city': record.city,
                            'state': record.state,
                            'effective': record.effective,
                            'press_release': record.press_release
                        }
                    )
                    change_count += 1
        else:
            self.stdout.write("No previous pull found for comparison")
        
        # Mark pull as processed
        current_pull.is_processed = True
        current_pull.save()
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully processed {len(current_data)} records with {change_count} changes'
        ))