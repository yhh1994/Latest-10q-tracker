import urllib.request
import json

def generate_sp500_json():
    # SEC official ticker to CIK mapping file
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {'User-Agent': 'My10QTracker (db4ads@gmail.com)'}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        raw_data = json.loads(response.read().decode('utf-8'))

    sp500_list = []
    
    # Process all entries from the SEC master company list
    for entry in raw_data.values():
        cik_str = str(entry['cik_str']).zfill(10) # SEC CIKs must be 10 digits zero-padded
        sp500_list.append({
            "ticker": entry['ticker'],
            "cik": cik_str,
            "name": entry['title']
        })

    # Sort alphabetically by ticker
    sp500_list.sort(key=lambda x: x['ticker'])

    with open('sp500.json', 'w') as f:
        json.dump(sp500_list, f, indent=2)

    print(f"Successfully generated sp500.json with {len(sp500_list)} companies.")

if __name__ == "__main__":
    generate_sp500_json()
