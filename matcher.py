
import pandas as pd
import re
import json
from search_scraper import scrape_new_format,scrape_old_format
# brief_mapping is a json dictionary maps a filename to a docket 
brief_mapping = json.load(open("data/filename-to-docket.json"))
#declare result mapping Docket# -> result information
result_mapping = {}

# these next 4 lines fill out result mapping with the current up-to-date data
for line in open("data/search_scrapings.txt","r").read().split("\n"):
    split_line = line.split("->")
    #layout docket# -> result info
    if len(split_line) > 1:
        #without eval it is a string
        result_mapping[split_line[0]] = str(split_line[1])

def docket_match(LIWCdata,brief_reference,result_reference,tableinfodata):
    #LIWCdata is dataframe with filename, and the liwc columns
    #brief_reference is dictionary maps filename to docket#
    # result_reference dictionary maps docket# to result
    #tableinfodata scraped opinion information
    
    #creates data frame liwc data
    LIWC = pd.read_csv(LIWCdata)
    tableinfofile = pd.read_csv(tableinfodata)
    
    # D1 = dimension1 -> what row of the csv file you are on
    docket_number_column = []
    result_column = []
    for D1,row in LIWC.iterrows():
        filename = row["Filename"]
        
        try:
            docket_number = brief_reference[filename]
            result = result_reference[docket_number]
            docket_number_column.append(docket_number)
            result_column.append(result)
        except Exception as e:
            docket_number_column.append("")
            result_column.append("")
            print(e)
        
        '''
        for D2,cell in tableinfofile.iterrows():
            #brief reference is brief_mapping
            filename = row["Filename"]

            if(brief_reference[filename] == cell["Docket"]):

                #has to get into liwc table
                result = str(result_reference[cell["Docket"]])
                docket_number = str(cell["Docket"])
                LIWC_filename = filename

                count += 1

                datboi = "LIWC file #"+str(D1)+" & scotus opinion #"+str(D2)+" matched on " + str(cell["Docket"])
                try:
                    datboi += " with results:" + str(result_reference[cell["Docket"]])
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
                print(datboi)
            '''
    #print(docket_number_column)
    #print(result_column)
    LIWC["docket_number"] = docket_number_column
    LIWC["result"] = result_column

    LIWC.to_csv("data.csv",index=False)



if __name__ == "__main__":
    docket_match("data/liwcbriefs.csv",brief_mapping,result_mapping,"data/table.csv")
    