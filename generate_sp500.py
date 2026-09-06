import pandas as pd
import json

def generate_sp500_json():
    wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # pandas natively parses the HTML tables on the page
    tables = pd.read_html(wiki_url)
    
    # The first table on that Wikipedia page is the main constituents table
    df = tables[0]
    
    sp500_list = []
    
    for _, row in df.iterrows():
        # Clean up tickers like BRK.B to BRK-B
        ticker = str(row['Symbol']).replace('.', '-')
        name = str(row['Security'])
        cik_str = str(row['CIK']).zfill(10)
        
        sp500_list.append({
            "ticker": ticker,
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
