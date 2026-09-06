import urllib.request
import json
import re

def generate_sp500_json():
    # 1. Fetch current S&P 500 tickers and CIKs directly from Wikipedia's list
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    req = urllib.request.Request(
        wiki_url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')

    # Parse ticker and CIK pairs from the S&P 500 table HTML
    # Matches patterns like: edgar/data/0000320193 and ticker symbol links
    pattern = r'<td><a rel="nofollow" class="external text" href="https://www\.sec\.gov/edgar/browse/\?CIK=(\d+)">([^<]+)</a></td>\s*<td><a href="[^"]+" title="([^"]+)">'
    matches = re.findall(pattern, html)

    sp500_list = []
    seen_ciks = set()

    for cik, ticker, name in matches:
        cik_str = cik.zfill(10) # Format CIK to standard 10-digit zero-padded string
        if cik_str not in seen_ciks:
            seen_ciks.add(cik_str)
            sp500_list.append({
                "ticker": ticker.replace('.', '-'), # Format BRK.B to BRK-B
                "cik": cik_str,
                "name": name
            })

    # Sort alphabetically by ticker
    sp500_list.sort(key=lambda x: x['ticker'])

    with open('sp500.json', 'w') as f:
        json.dump(sp500_list, f, indent=2)

    print(f"Successfully generated sp500.json with {len(sp500_list)} S&P 500 companies.")

if __name__ == "__main__":
    generate_sp500_json()
