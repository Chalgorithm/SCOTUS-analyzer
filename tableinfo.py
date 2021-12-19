import pandas as pd
import requests
from bs4 import BeautifulSoup


# https://stackoverflow.com/questions/47561116/scrape-webpage-containing-before
# https://stackoverflow.com/questions/44704099/python-scrape-table-from-website
# https://stackoverflow.com/questions/34250552/python-beautifulsoup-to-scrape-tables-from-a-webpage
# https://stackoverflow.com/questions/41569480/scrape-tables-with-python

for page in range(21,20,-1):
        
        r = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2)) # zfill so if it is 5, it becomes 05, zfill of 2 makes sure length is 2.
        
        html = r.text

        soup = BeautifulSoup(html)
        table = soup.find('table', {"class": "table table-bordered"})
        rows = table.find_all('tr')
        data = []
        for row in rows[0:]:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

        result = pd.DataFrame(data, columns=['R-','Date','Docket','Name','Revised','J.','Pt.'])

        print(result)
