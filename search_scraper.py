import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from itertools import islice


def scrape_search():
    with open("data/search_scrapings.txt","a") as output_file:
        opinion_table = pd.read_csv("data/table.csv")
        startOfIndex = 350
        for index, row in islice(opinion_table.iterrows(), startOfIndex, None):
            result = "None"
            docket_number = row["Docket"]
            try:
                print(str(docket_number)+"->"+str(scrape_any(docket_number)))
            except Exception as e:
                print(e)
            """
            try:

                
                # result = scrape_old_format(docket_number)
                # print(result)
                result = scrape_new_format(docket_number)
                print({docket_number:result})
                output_file.write(docket_number +"->" +str(result)+"\n")
            except Exception as e:
                try:
                    
                    result = scrape_old_format(docket_number)
                    print({docket_number:result})
                    output_file.write(docket_number +"->"+str(result)+"\n")
                except:
                    print("can't get docket#")
                print(e)
            """
            

    #docket_number = "02-6683"
    #new_docket_number = "19-897"
    #scrape_new_format(new_docket_number)
    
    #scrape_old_format(docket_number)
    
def scrape_any(docket_number):
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm")
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