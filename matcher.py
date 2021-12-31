
import pandas as pd
import re
import json
from search_scraper import scrape_new_format,scrape_old_format

mapping = json.load(open("data/filename-to-docket.json"))


def docket_match(LIWCfile,brief_reference,opinionfile):
    count = 0
    LIWC = pd.read_csv(LIWCfile)
    opinionfile = pd.read_csv(opinionfile)
    for D1,row in LIWC.iterrows():
        for D2,cell in opinionfile.iterrows():
            if(mapping[row["Filename"]] == cell["Docket"]):
                count += 1
                print("LIWC file #"+str(D1)+" & scotus opinion #"+str(D2)+" matched on " + str(cell["Docket"]))
    print("count = "+str(count))



         




if __name__ == "__main__":
    docket_match("data/liwcbriefs.csv",mapping,"data/table.csv")
    