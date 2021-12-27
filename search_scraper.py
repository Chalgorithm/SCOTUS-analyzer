import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def scrape_search():
    #get document
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/19-62.html")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    docketinfo = soup.find('table', id='docketinfo')
    proceedings = soup.find('table', id='proceedings')
    print(docketinfo)
    print(proceedings)
    


if __name__ == "__main__":
    pass