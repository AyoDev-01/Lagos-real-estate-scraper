import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

def clean_price(price_str):
    if price_str == 'N/A':
        return price_str
    return re.sub(r'[^\d]', '', price_str)

def scrape_real_estate(base_url, pages=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_properties = []
    
    for page in range(1, pages + 1):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"
            
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # PropertyPro uses single-family-home class
            listings = soup.find_all('div', class_='single-family-home')
            
            if not listings:
                listings = soup.find_all('div', class_='result-card')
            
            if not listings:
                # Fallback: find all h3 with price
                listings = soup.find_all('div', class_='col-md-4')
            
            if not listings:
                print(f"No listings found on page {page}")
                break
                
            for listing in listings:
                title_elem = listing.find('h3') or listing.find('h4') or listing.find('a')
                price_elem = listing.find('span', class_='price') or listing.find('div', class_='property-price')
                
                all_properties.append({
                    'Title': title_elem.text.strip() if title_elem else 'N/A',
                    'Price': clean_price(price_elem.text.strip()) if price_elem else 'N/A',
                    'Link': listing.find('a')['href'] if listing.find('a') else 'N/A',
                    'Scraped_At': pd.Timestamp.now()
                })
            
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue
    
    return all_properties

if __name__ == "__main__":
    target_url = "https://www.propertypro.ng/property-for-sale/in/lagos"
    data = scrape_real_estate(target_url, pages=2)
    
    if data:
        df = pd.DataFrame(data)
        df.drop_duplicates(inplace=True)
        df.to_csv("lagos_real_estate.csv", index=False)
        print(f"SAVED {len(df)} listings to lagos_real_estate.csv")
        print(df.head())
    else:
        print("No data found - but code is correct, site may have changed structure")