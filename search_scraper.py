import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_search():
    docket_number = "02-6683"
    new_docket_number = "21-463"
    #scrape_new_format(new_docket_number)
    
    scrape_old_format(docket_number)
    

def scrape_new_format(docket_number):
    #get document
    result_options = [r"AFFIRMED",r"REMANDED",r"VACATED",r"REVERSED"]
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/" + str(docket_number) + ".html")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings = soup.find("table", id="proceedings")
    print(proceedings)
    for tablerow in proceedings.find_all("borderbttm"):   
        for data in tablerow:
            print(data.find('a', href=True, text="Petition", class_="documentanchor"))
            
   


def scrape_old_format(docket_number):
    result_options = [r"AFFIRMED",r"REMANDED",r"VACATED",r"REVERSED"]
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings_body = soup.find("tbody")
    for row in proceedings_body.find_all("tr"):
        proceedings = row.find_all("td")
        content = proceedings[1].text
        for result in result_options:
            matches = re.search(result,content) is not None
            print(matches)
        #prefixmatches = re.search(prefix,str(current_line)) is not None
        
        
        
            
            
    


if __name__ == "__main__":
    scrape_search()