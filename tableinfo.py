from http.client import responses
from logging import exception
from requests.api import head
from requests.models import HTTPError
import re
import requests
from bs4 import BeautifulSoup
import time
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams
import os
import re
import pandas as pd
   

def scrape_opinions():


    # sample headers from the internet
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    

    for page in range(21,20,-1):
        response = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2)) # zfill so if it is 5, it becomes 05, zfill of 2 makes sure length is 2.
            
        soup = BeautifulSoup(response.content,"lxml")
        
        table1 = soup.find('div', id="list")
        headers = []

        for i in table1.find_all('table'):
                title = i.text
                
                headers.append(title)

        print(headers)

'''

for j in table1.find_all('tbody'):
    for k in table1.find_all('th'):

'''

if __name__ == "__main__":
  scrape_opinions()
