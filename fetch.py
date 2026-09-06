import urllib.request
import xml.etree.ElementTree as ET
import json

def fetch_latest_10qs():
    # The SEC RSS feed for the 50 most recent 10-Q filings
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=10-Q&count=50&output=atom'
    
    # IMPORTANT: Replace the email address below with your actual email.
    # The SEC will block your request if you do not provide a valid User-Agent.
    headers = {
        'User-Agent': 'My10QTracker (db4ads@gmail.com)'
    }

    try:
        # Request the data from the SEC
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read()

        # Parse the XML response
        root = ET.fromstring(content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        filings = []
        
        # Loop through each filing entry in the feed
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:link', ns).attrib['href']
            updated = entry.find('atom:updated', ns).text
            
            filings.append({
                'title': title,
                'link': link,
                'date': updated
            })

        # Save the extracted data to data.json
        with open('data.json', 'w') as f:
            json.dump(filings, f, indent=2)
            
        print(f"Successfully saved {len(filings)} filings to data.json")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_latest_10qs()
