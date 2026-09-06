import urllib.request
import json
import time
from datetime import datetime, timedelta

def fetch_sp500_historical_10qs():
    # Load S&P 500 list
    try:
        with open('sp500.json', 'r') as f:
            sp500_companies = json.load(f)
    except FileNotFoundError:
        print("sp500.json not found. Please create it first.")
        return

    # Calculate date threshold (3 years ago from today)
    three_years_ago = (datetime.now() - timedelta(days=3*365)).strftime('%Y-%m-%d')
    
    headers = {
        'User-Agent': 'My10QTracker (your.real.email@example.com)'  # Keep your email updated here
    }

    all_filings = []

    for comp in sp500_companies:
        cik = comp['cik']
        ticker = comp['ticker']
        company_name = comp['name']
        
        url = f'https://data.sec.gov/submissions/CIK{cik}.json'
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Extract recent filings array from SEC payload
            recent = data.get('filings', {}).get('recent', {})
            forms = recent.get('form', [])
            filing_dates = recent.get('filingDate', [])
            accession_numbers = recent.get('accessionNumber', [])
            primary_documents = recent.get('primaryDocument', [])

            for i in range(len(forms)):
                form_type = forms[i]
                f_date = filing_dates[i]

                # Filter for 10-Q forms filed within the last 3 years
                if form_type == '10-Q' and f_date >= three_years_ago:
                    acc_no_clean = accession_numbers[i].replace('-', '')
                    doc = primary_documents[i]
                    
                    # Construct direct SEC EDGAR URL
                    link = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_clean}/{doc}"
                    
                    all_filings.append({
                        'title': f"10-Q - {ticker} ({company_name})",
                        'ticker': ticker,
                        'link': link,
                        'date': f_date
                    })

            # SEC rate limits require maximum 10 requests per second
            time.sleep(0.12)

        except Exception as e:
            print(f"Error fetching CIK {cik} ({ticker}): {e}")

    # Sort all filings descending by filing date
    all_filings.sort(key=lambda x: x['date'], reverse=True)

    # Save to data.json
    with open('data.json', 'w') as f:
        json.dump(all_filings, f, indent=2)

    print(f"Successfully saved {len(all_filings)} filings from the last 3 years.")

if __name__ == "__main__":
    fetch_sp500_historical_10qs()
