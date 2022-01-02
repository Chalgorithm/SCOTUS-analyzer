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
<<<<<<< HEAD
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
=======
                print(e)
>>>>>>> ab3f074b44006b25baa29a8c4586c8fa89c92a2c
            

    #docket_number = "02-6683"
    #new_docket_number = "19-897"
    #scrape_new_format(new_docket_number)
    
    #scrape_old_format(docket_number)
    
<<<<<<< HEAD

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

def scrape_any(link):
=======
def scrape_any(docket_number):
>>>>>>> ab3f074b44006b25baa29a8c4586c8fa89c92a2c
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