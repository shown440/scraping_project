import hashlib
import json
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from django.utils import timezone
from app_scrap.models import DataPull, CIAData, DataChange

logger = logging.getLogger(__name__)







def parse_cia_data():
    base_url = "https://oig.hhs.gov/compliance/corporate-integrity-agreements/cia-documents.asp#"
    all_data = []
    
    letters = [chr(i) for i in range(97, 123)]  # a to z
    
    my_var = 0
    for letter in letters:
        url = f"{base_url}{letter}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        cia_table = soup.find('table', {'id': 'cia_list'})
        
        if not cia_table:
            continue
            
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
    data_str = f"{record['provider']}|{record['city']}|{record['state']}|{record['effective']}|{record['press_release']}"
    return hashlib.sha256(data_str.encode()).hexdigest()


def fetch_and_process_cia_data():
    """
    Fetches CIA data, processes it, and stores changes
    Returns tuple: (success: bool, message: str)
    """
    try:
        logger.info("Starting CIA data processing")
        current_pull = DataPull.objects.create()
        logger.info(f"Created DataPull ID: {current_pull.id}")

        current_data = parse_cia_data()
        logger.info(f"Fetched {len(current_data)} records")
        
        current_hashes = set()
        change_count = 0

        for record in current_data:
            record_hash = generate_record_hash(record)
            current_hashes.add(record_hash)
            CIAData.objects.create(
                data_pull=current_pull,
                record_hash=record_hash,
                **record
            )

        previous_pull = DataPull.objects.filter(is_processed=True).order_by('-pull_time').first()
        
        if previous_pull:
            logger.info(f"Comparing with previous pull ID: {previous_pull.id}")
            previous_hashes = set(CIAData.objects.filter(
                data_pull=previous_pull
            ).values_list('record_hash', flat=True))

            # Find added records
            added_hashes = current_hashes - previous_hashes
            for record in current_data:
                if generate_record_hash(record) in added_hashes:
                    DataChange.objects.create(
                        data_pull=current_pull,
                        change_type='added',
                        provider=record['provider'],
                        current_data=record
                    )
                    change_count += 1

            # Find removed records
            removed_hashes = previous_hashes - current_hashes
            for record in CIAData.objects.filter(record_hash__in=removed_hashes):
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

        current_pull.is_processed = True
        current_pull.save()

        msg = f"Processed {len(current_data)} records with {change_count} changes"
        logger.info(msg)
        return True, msg
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return False, f"Error occurred: {str(e)}"