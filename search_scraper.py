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
    

def scrape_new_format(docket_number):
    #get document
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/" + str(docket_number) + ".html")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings_body = soup.find("table", id="proceedings")
    '''
    petition = proceedings_body.find('a', href=True, text="Petition", class_="documentanchor")
    opinion = proceedings_body.find('a', href=True, text="opinion")
    petitionlink = petition['href']
    opinionlink = opinion['href']
    
    for row in proceedings_body.find_all("tr"):
        proceedings = row.find_all("td")
        content = proceedings[1].text.strip()
    '''
    content = proceedings_body.text.strip()
    return result_scan(content)

def scrape_any(docket_number):
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm")
    print(r)
    html = r.text
    soup = BeautifulSoup(r.content, features="lxml")
    #print(soup.contents)
    return result_sentence(soup.contents)


def scrape_old_format(docket_number):
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm")
    print(r)
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings_body = soup.find("tbody")
    for row in proceedings_body.find_all("tr"):
        print(row)
        proceedings = row.find_all("td")
        content = proceedings[1].strip()
        return result_scan(content)

def result_sentence(pagetext):
    regex = r"([A-Z][A-Za-z ,]*(AFFIRMED|REVERSED|REMANDED|VACATED|DISMISSED|DENIED)+([A-Za-z ,]*)\.)"
    match = re.search(regex,str(pagetext))
    if match != None:
        m = match.group(1)
        return m


        
def result_scan(content):
    result_options = [r"AFFIRM",r"REMAND",r"VACATE",r"REVERSE",r"DISMISS"]
    output_results = {}
    last_token = ""
    for token in content.split(" "):
        for r_i in range(0,len(result_options)):
            expression = result_options[r_i]
            matches = re.search(expression,token) is not None
            # store dictionary of previous word and return
            if matches:
                output_results[last_token] = r_i
        last_token = token

    return output_results
   

        
        
    


if __name__ == "__main__":
    scrape_search()