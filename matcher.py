
import pandas as pd
import re
import json

#df_json = pd.read_json("data/doj_briefs.json", orient="index").reset_index()

with open("data/doj_briefs.json","r") as json_file:
    json_data = json.load(json_file)

def generate_brief_reference(json_data):
    for key, value in json_data.items():
        name = key.split("/")[-1]
        print(name)

def docket_match(LIWCfile,brief_reference,opinionfile):

    LIWC = pd.read_csv(LIWCfile)
    opinionfile = pd.read_csv(opinionfile)


         




if __name__ == "__main__":
    docket_match("data/liwcbriefs.csv",json_data,"data/table.csv")
    generate_brief_reference(json_data)