import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import requests
import time

# Alex Wang, Christopher Haley (2021/12/20) Revision 1
# Alex Wang, Revision 2 (2021/12/23)
data = []

for page in range(21,2,-1): # goes back to 2004
        time.sleep(0.3) # to prevent DDosing the site lmao
        r = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2)) # zfill so if it is 5, it becomes 05, zfill of 2 makes sure length is 2.
        
        html = r.text

        soup = BeautifulSoup(html, features="lxml")
        divs = soup.findAll('div', "panel panel-default")
        

        for div in divs:
                div.find()
                table = div.find('table', {"class": "table table-bordered"})
                rows = table.find_all('tr')
                for row in rows[0:]:
                        try: 
                                columns = row.find_all('td') # td -> table data
                                elements = []
                                for element in columns:                                  
                                        elements.append(element.text)
                                
                        except:
                                pass
           
                        if(len(elements) == 7):
                                data.append(elements)
                        else:
                                elements.insert(4, " ")
                                data.append(elements)

result = pd.DataFrame(data, columns=['R-','Date','Docket','Name','Revised','J.','Pt.'])   
result.dropna(subset = ["Name"], inplace=True)
result.to_csv('table.csv', index=False, encoding='utf-8')

