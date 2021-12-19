import pandas as pd
import requests
from bs4 import BeautifulSoup

for page in range(21,5,-1):
        
        # response = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2)) # zfill so if it is 5, it becomes 05, zfill of 2 makes sure length is 2.
        url = 'https://www.supremecourt.gov/opinions/slipopinion/21'

        r = requests.get(url)
        html = r.text

        soup = BeautifulSoup(html)
        table = soup.find('table', {"class": "t-chart"})
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

        result = pd.DataFrame(data, columns=['R-','Date','Docket','Name','Revised','J.','Pt.'])

        print(result)
