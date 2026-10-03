import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

def clean_price(price_str):
    # Business wants numbers, not "₦ 50,000,000" -> 50000000
    if price_str == 'N/A': return price_str
    return re.sub(r'[^\d]', '', price_str)

def scrape_real_estate(base_url, pages=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
    }
    
    all_properties = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"  # Pagination
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            listings = soup.find_all('div', class_='listing-card') # CHANGE THIS
            
            if not listings:
                print(f"No listings on page {page}, stopping.")
                break
                
            for listing in listings:
                all_properties.append({
                    'Title': listing.find('h2', class_='property-title').text.strip() if listing.find('h2', class_='property-title') else 'N/A',
                    'Price': clean_price(listing.find('span', class_='property-price').text.strip()) if listing.find('span', class_='property-price') else 'N/A',
                    'Address': listing.find('div', class_='property-address').text.strip() if listing.find('div', class_='property-address') else 'N/A',
                    'Link': listing.find('a')['href'] if listing.find('a') else 'N/A',
                    'Scraped_At': pd.Timestamp.now()
                })
            
            # Anti-blocking: random sleep
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue
    
    return all_properties

if __name__ == "__main__":
    target_url = "https://www.privateproperty.com.ng/for-sale/lagos" # REAL site
    data = scrape_real_estate(target_url, pages=5)
    
    if data:
        df = pd.DataFrame(data)
        df.drop_duplicates(inplace=True)
        df.to_csv("lagos_real_estate.csv", index=False)
        print(f"Saved {len(df)} listings")