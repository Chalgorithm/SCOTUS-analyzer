from http.client import responses
from logging import exception
from requests.models import HTTPError
from pdfmining import process_document
import re
import requests
from bs4 import BeautifulSoup
import threading
import time

from concurrent.futures import ThreadPoolExecutor

#author: Christopher Haley


def scrape_opinions():
    # sample headers from the internet
    headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    with ThreadPoolExecutor(max_workers=6) as e:

        for page in range(21,5,-1):
            response = requests.get("https://www.supremecourt.gov/opinions/slipopinion/"+str(page).zfill(2),headers)
            
            soup = BeautifulSoup(response.content,"html.parser")
            #table = soup.find("table",{"class":""})
            
            for anchor_tag in soup.findAll('a'):
                if(re.search(r".pdf$",str(anchor_tag.get('href'))) is not None):
                    
                    link = "https://www.supremecourt.gov" + str(anchor_tag.get('href'))
                    try:
                        time.sleep(0.3)
                        response = requests.get(link)
                        title = anchor_tag.text
                        e.submit(process_document,title,response)
                        
                    except UnicodeError:
                        pass
                
            
if __name__ == "__main__":
    scrape_opinions()
    
    
    
    