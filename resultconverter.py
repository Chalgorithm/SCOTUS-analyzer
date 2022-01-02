import re
import pandas as pd
from itertools import islice


data = pd.read_csv("data/data.csv")

def data_cleaner(datafile):
    result_options = [r"AFFIRMED",r"REMANDED",r"VACATED",r"REVERSED",r"DISMISSED",r"DENIED"]
    part_options = r" IN PART"
    date_options = r"(0[5-9]|1[0-9]|2[0-1])-[0-9]{2,4}"
    output_results = ""
    result_list = []
    partial_list = []
    listOfIndexs = []

    startOfIndex = 0
    for index, row in islice(datafile.iterrows(), startOfIndex, None):
        output_string = ""
        partial_output_string = ""
        for r_i in range(0,len(result_options)):
            expression = result_options[r_i]
            matches = re.search(expression,str(row["result"])) is not None
            date_matches = re.search(date_options,str(row["docket_number"]))
            if matches:
                if re.search(expression + part_options, str(row["result"])) is not None:
                    partial_output_string += str(r_i) + " "
                else:
                    output_string += str(r_i) + " "
        if not date_matches:
            listOfIndexs.append(index)

        partial_list.append(partial_output_string)
        result_list.append(output_string)
        
    
    data["result_int"] = result_list
    data["partial_result"] = partial_list 
    data1 = data.drop(data.index[listOfIndexs])
    data1.to_csv("data_clean.csv",index=False)


if __name__ == "__main__":
    data_cleaner(data)
