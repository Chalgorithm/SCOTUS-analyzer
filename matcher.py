
import pandas as pd
import re
import json
from search_scraper import scrape_new_format,scrape_old_format

brief_mapping = json.load(open("data/filename-to-docket.json"))

result_mapping = {}

for line in open("data/search_scrapings.txt","r").read().split("\n"):
    split_line = line.split("->")
    if len(split_line) > 1:
        result_mapping[split_line[0]] = eval(split_line[1])

def docket_match(LIWCfile,brief_reference,result_reference,opinionfile):
    count = 0
    LIWC = pd.read_csv(LIWCfile)
    opinionfile = pd.read_csv(opinionfile)
    for D1,row in LIWC.iterrows():
        for D2,cell in opinionfile.iterrows():
            if(brief_reference[row["Filename"]] == cell["Docket"]):
                count += 1

                datboi = "LIWC file #"+str(D1)+" & scotus opinion #"+str(D2)+" matched on " + str(cell["Docket"])
                try:
                    datboi += " with results:" + str(result_reference[cell["Docket"]])
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
                print(datboi)
    print("count = "+str(count))



         




if __name__ == "__main__":
    docket_match("data/liwcbriefs.csv",brief_mapping,result_mapping,"data/table.csv")
    