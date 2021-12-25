import pandas as pd

scraped_results = {}
def initialize():
    court_scrapings = open("results.txt","r")
    for line in court_scrapings:
        case = line.split(",[")[0]
        end = len(case)+1
        results = eval(line[end:].rstrip())
        scraped_results[case] = results
    print(scraped_results)





def process_site_items():
    meta_scrapings = pd.read_csv("table.csv")
    results = ["affirmed","remanded","vacate","reversed","none detected","affirmed in part","remanded in part","vacated in part","reversed in part"]
    for rnum in range(0,len(results)):
        meta_scrapings.insert(7+rnum,results[rnum],"no")
    data = []
    for index, row in meta_scrapings.iterrows():
        try:
            positives = [i for i in map(lambda x: results[x],scraped_results[row["Name"]])]
            print(positives)
            for res in positives:
                row[res] = "yes"
            data.append(row)
        except KeyError:
            print(row["Name"]+": not found in results.txt")
        
        
    result = pd.DataFrame(data, columns=['R-','Date','Docket','Name','Revised','J.','Pt.',"affirmed","remanded","vacate","reversed","none detected","affirmed in part","remanded in part","vacated in part","reversed in part"])   
    result.dropna(subset = ["Name"], inplace=True)
    result.to_csv('results_data.csv', index=False, encoding='utf-8')
    



        
initialize()
process_site_items()