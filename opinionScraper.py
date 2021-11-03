
from http.client import responses
from logging import exception
from requests.models import HTTPError
from tika import parser
import re
import requests
from bs4 import BeautifulSoup
import threading
import time
from concurrent.futures import ThreadPoolExecutor
#author: Christopher Haley

def inorder(results):
    for r in results:
        if any([r < a for a in results[:results.index(r)-1]]):
            return results[:results.index(r)]
    return results

def case_classify(opinion_file):
    try:
        raw_text = parser.from_buffer(opinion_file)['content']
    except:
        return [4]
    
    #Case Result? (4 = Other; 3 = reversed; 2 = vacate; 1 = remanded; 0 = affirmed)
    result_options = [r"affirmed",r"remanded",r"vacate",r"reversed"]
    
    prefix = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)"
    whole = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)\.( )*$"
    suffix = r"^(.*)\.(.*)$"
    end_of_syllabus = r"Opinion(.*)\."

    results = []
    # algorithm looks for verdict
    #pattern matching by docket number:
    lastline = ""
    
    for line in raw_text.split("\n"):
        #pattern matching verdict:
        for word in result_options:
            prefixmatches = re.search(prefix,line) is not None
            llprefixmatches = re.search(prefix,lastline) is not None
            suffixmatches = re.search(suffix,line) is not None
            matches = re.search(word,line) is not None
            if(prefixmatches and matches):
                results.append(result_options.index(word))
            elif(llprefixmatches and matches):
                results.append(result_options.index(word))
                print(line)
                '''   
                elif(matches and suffixmatches):
                    results.append(result_options.index(word))
                '''
        lastline = line     
                

        

            
                

    output = results
    if(len(output) == 0):
        output = [4]
    print(str(opinion_file.url) + " results: " + str(output))
    return output

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
            for anchor_tag in soup.findAll('a'):
                if(re.search(r".pdf$",str(anchor_tag.get('href'))) is not None):
                    link = "https://www.supremecourt.gov" + str(anchor_tag.get('href'))
                    try:
                        time.sleep(0.3)
                        response = requests.get(link)
                        e.submit(case_classify,response)
                        
                    except UnicodeError:
                        pass
                
                
                
            
if __name__ == "__main__":
    scrape_opinions()
    
    
    
    