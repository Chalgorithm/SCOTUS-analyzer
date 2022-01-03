import re
import pandas as pd
from itertools import islice


data = pd.read_csv("data/data.csv")

def data_cleaner(datafile):
    result_options = [r"AFFIRMED",r"REMANDED",r"VACATED",r"REVERSED",r"DISMISSED",r"DENIED"]
    # remanded can be seperate column
    # 0 AFFIRMED
    # 1 should be reversed/ vacated
    # 2 should be anything else
    # 3 is DENIED
    # remanded column is 0 = "is remanded", 1 = "not remanded", 2 = "IN PART"
    # result_options = [r"AFFIRMED",r"REVERSED"]
    part_options = r" IN PART"
    date_options = r"(0[5-9]|1[0-9]|2[0-1])-[0-9]{2,4}"
    output_results = ""
    
    #column lists
    result_column = []
    remanded_column = []
    result_text_column = []


    listOfIndexs = []

    startOfIndex = 0
    enumeration = 12
    memo = {}
    for index, row in islice(datafile.iterrows(), startOfIndex, None):
        
        result_output = 2
        remanded_output = 0
        #partial_output_string = ""
        #for r_i in range(0,len(result_options)):
            #expression = result_options[r_i]
        result_text_column.append(str(row["result"]))
        aff_matches = re.search(r"AFFIRMED(?! IN PART)",str(row["result"])) is not None
        rev_matches = re.search(r"(REVERSED(?! IN PART)|VACATED(?! IN PART))",str(row["result"])) is not None
        rem_matches = re.search(r"(REMANDED(?! IN PART))",str(row["result"])) is not None
        rem_part_matches = re.search(r"(REMANDED IN PART)",str(row["result"])) is not None
        den_matches = re.search(r"DENIED(?! IN PART)",str(row["result"])) is not None
        date_matches = re.search(date_options,str(row["docket_number"]))
        
        if aff_matches and not rev_matches:
            result_output = 0
        elif rev_matches and not aff_matches:
            result_output = 1
        elif den_matches:
            result_output = 3
        
        if rem_matches:
            remanded_output = 1
        elif rem_part_matches:
            remanded_output = 2
        result_column.append(result_output)
        remanded_column.append(remanded_output)

                
                    
                    
                    
        if not date_matches:
            listOfIndexs.append(index)

        #partial_list.append(partial_output_string)
    data["remanded"] = remanded_column
    data["result text"] = result_text_column
    data["result"] = result_column
    
    
    data1 = data.drop(data.index[listOfIndexs])
    data1.to_csv("data_clean.csv",index=False)


if __name__ == "__main__":
    data_cleaner(data)
