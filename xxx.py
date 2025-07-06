import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_cia_data(url):
    """Parse CIA data from a given URL"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    cia_table = soup.find('table', {'id': 'cia_list'})
    
    data = []
    if cia_table:
        for row in cia_table.find_all('tr'):
            # Skip header rows
            if row.find('th') or not row.find('td'):
                continue
                
            columns = row.find_all('td')
            if len(columns) >= 5:
                # Extract provider text
                provider = columns[0].get_text(strip=True)
                
                # Extract press release link if available
                press_release = columns[4].find('a')
                press_release_link = press_release['href'] if press_release else None
                
                data.append({
                    'Provider': provider,
                    'City': columns[1].get_text(strip=True),
                    'State': columns[2].get_text(strip=True),
                    'Effective': columns[3].get_text(strip=True),
                    'Press Release': press_release_link
                })
    return data

def get_all_cia_data():
    """Get CIA data for all letters A-Z"""
    base_url = "https://oig.hhs.gov/compliance/corporate-integrity-agreements/cia-documents.asp#"
    all_data = []
    
    # Letters to process (A-Z)
    letters = [chr(i) for i in range(97, 123)]  # a to z
    
    for letter in letters:
        url = f"{base_url}{letter}"
        print(f"Processing: {url}")
        letter_data = parse_cia_data(url)
        all_data.extend(letter_data)
    
    return all_data

# Main execution
if __name__ == "__main__":
    cia_data = get_all_cia_data()
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(cia_data)
    df.to_csv('cia_data.csv', index=False)
    print(f"Saved {len(df)} records to cia_data.csv")
    
    # Print sample data
    print("\nSample data:")
    print(df.head())