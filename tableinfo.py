import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests
import time

# Alex Wang, Christopher Haley (2021/12/20) Revision 1

for page in range(21,2,-1): # goes back to 2004
        time.sleep(0.3) # to prevent DDosing the site lmao
        r = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2)) # zfill so if it is 5, it becomes 05, zfill of 2 makes sure length is 2.
        
        html = r.text

        soup = BeautifulSoup(html, features="lxml")
        table = soup.find('table', {"class": "table table-bordered"})
        rows = table.find_all('tr')
        data = []
        

        for row in rows[0:]:
                try:
                        columns = row.find_all('td') # td -> table data
                        elements = []
                        for element in columns:
                                if(element.text == ""):
                                        elements.append("None")
                                else:                                        
                                        elements.append(element.text)
                        if(len(elements) == 7):
                                data.append(elements)
                        else:
                                elements.insert(4, "None")
                                data.append(elements)
                              
                except:
                        pass
           

        result = pd.DataFrame(data, columns=['R-','Date','Docket','Name','Revised','J.','Pt.'])
      
        print(result)
