import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from itertools import islice


def scrape_search():
    
    opinion_table = pd.read_csv("data/table.csv")
    with open('data/filename-to-docket.json') as json_file:
        dockets = json.load(json_file)
    
    startOfIndex = 0
    #for index, row in islice(opinion_table.iterrows(), startOfIndex, None):
    for docknum in dockets.values():
        result = "None"
        docket_number = docknum
        try:
        
            try:
                with open("data/search_scrapings3.txt","a") as output_file:
                    link = "https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/" + str(docket_number) + ".html"
                    if scrape_any(link) == None:
                        link = "https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm"
                        
                    output_file.write(str(docket_number)+"->"+str(scrape_any(link))+"\n")
                    output_file.close()
            except Exception as e:
                try:
                    with open("data/search_scrapings3.txt","a") as output_file:
                        link = "https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm"
                        print(scrape_any(link))
                        output_file.write(str(docket_number)+"->"+str(scrape_any(link))+"\n")
                        output_file.close()
                except Exception as d:
                    pass
        except Exception as e:
            print(e)

def scrape_any(docket_number):

    time.sleep(0.3)
    r = requests.get(link)
    print(r)
    html = r.text
    soup = BeautifulSoup(r.content, features="lxml")
    #print(soup.contents)
    return result_sentence(soup.contents)


def result_sentence(pagetext):
    regex = r"([A-Z][A-Za-z ,]*(AFFIRMED|REVERSED|REMANDED|VACATED|DISMISSED|DENIED)+([A-Za-z ,]*)\.)"
    match = re.search(regex,str(pagetext))
    if match != None:
        m = match.group(1)
        return m

if __name__ == "__main__":
    scrape_search()