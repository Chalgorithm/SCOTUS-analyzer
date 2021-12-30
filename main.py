import pandas as pd

def historic_result(LIWCfile):
    # iterate through liwc file
    # provided with docket# find decision
    data = []
    output = pd.DataFrame(data, columns=["Filename","Judgement"])
    #add columns from liwc
    for column in LIWCfile:
        output[column] = []
    #iterate through liwc file
    for index, row in LIWCfile.iterrows():

    
    output.to_csv('results_data.csv', index=False, encoding='utf-8')
        



if __name__ == "__main__":
    #start: pass in liwc file
    LIWCfile = pd.read_csv("data/liwcbriefs.csv")
    historic_results(LIWCfile)