import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_search():
    opinion_table = pd.read_csv("data/table.csv")
    for index, row in opinion_table.iterrows():
        try:
            docket_number = row["Docket"]
            # result = scrape_old_format(docket_number)
            # print(result)
            newresult = scrape_new_format("19-897")
            print(newresult)
        except Exception as e:
            try:
                print(row["Docket"])
            except:
                print("can't get docket#")
            print(e)

    #docket_number = "02-6683"
    #new_docket_number = "21-463"
    #scrape_new_format(new_docket_number)
    
    #scrape_old_format(docket_number)
    

def scrape_new_format(docket_number):
    #get document
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/" + str(docket_number) + ".html")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings_body = soup.find("table", id="proceedings")
    proceedings = proceedings_body.find('a', href=True, text="Petition", class_="documentanchor")
    link = proceedings['href']
    content = proceedings_body.text.strip()
    return result_scan(content)
    # return result_scan(content)
   


def scrape_old_format(docket_number):
    time.sleep(0.3)
    r = requests.get("https://www.supremecourt.gov/search.aspx?filename=/docketfiles/"+str(docket_number)+".htm")
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    proceedings_body = soup.find("tbody")
    for row in proceedings_body.find_all("tr"):
        proceedings = row.find_all("td")
        content = proceedings[1].text
        return result_scan(content)
        
def result_scan(content):
    result_options = [r"AFFIRMED",r"REMANDED",r"VACATED",r"REVERSED",r"DISMISSED"]
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
                
       
        
        
            
            
    


if __name__ == "__main__":
    scrape_search()