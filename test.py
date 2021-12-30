import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re


time.sleep(0.3)
r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/21-463.html")
html = r.text
soup = BeautifulSoup(html, features="lxml")
proceedings = soup.find("table", id="proceedings")
print(proceedings.find('a', href=True, text="Petition", class_="documentanchor"))
        

           