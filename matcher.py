
import pandas as pd
import re

def match(LIWCfile,opinionfile):
    LIWC = pd.read_csv(LIWCfile)
    
    opinion = pd.read_csv(opinionfile)
    
    for indexL, LIWC_entry in LIWC.iterrows():
         liwc_title = extract_title(LIWC_entry["Filename"])
         for indexO, opinion_entry in opinion.iterrows():
            opinion_title = opinion_entry["Name"]
            if(liwc_title == opinion_title):
                #title matches
                print(liwc_title)
                break

         


def extract_title(celltext):
    clean_title = re.sub(r"-"," ", re.sub(r"\.[A-Za-z]{2,3}$","",celltext))
    return clean_title 

if __name__ == "__main__":
    match("data/liwcbriefs.csv","data/table.csv")

    print(extract_title("zuni-pubschdistno89-v-department-educ-opposition.txt"))