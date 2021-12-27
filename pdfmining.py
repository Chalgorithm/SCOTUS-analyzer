from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams
import os
import re
import requests
import time

def process_link(hyperlink):
    time.sleep(0.3)
    
    link = "https://www.supremecourt.gov"+str(hyperlink)
    response = requests.get(link)
    
    return process_document(response)

def process_document(response):
    counter = 0
    file = open(str(counter)+".pdf", 'wb').write(response.content)
    resultlist = extract_result(str(counter)+".pdf")
    outputlist = ["no" for i in range(0,10)]
    for result in resultlist:
        outputlist[result] = "yes"
    return outputlist

'''
def process_document(title,response):
    #lock.acquire()
    try:
      counter = 0
      file = open(str(counter)+".pdf", 'wb').write(response.content)
      result_entry = title +","+ str(extract_result(str(counter)+".pdf"))
    except Exception as e:
      result_entry = title +","+"[4]"
      print(e)
    print(result_entry)
    #scotus_writer.writerow(list(result_entry))
    #lock.release()
    output = open("results.txt", "a")  # append mode
    output.write(result_entry+"\n")
    output.close()
    
    #uncomment the line above to store all files
'''
def extract_result(path):
    
    
    result_options = [r"affirmed",r"remanded",r"vacate",r"reversed"]
    
    prefix = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)"
    whole = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)\.( )*$"
    suffix = r"^(.*)\.(.*)$"
    end_of_syllabus = r"Opinion(.*)\."

    case = ""
    results = []
    # algorithm looks for verdict
    #pattern matching by docket number:
    lastline = ""

    line_log = []
    index = 0
    for layout in extract_pages(path):
        for element in layout:
            if isinstance(element, LTTextContainer):
                for line in element:
                    for character in line:
                        if isinstance(character, LTChar):
                            font_size = character.size
                line_log.append((font_size,index,element.get_text()))
                index += 1
    second_header = [li for li in line_log if li[0] == 15.0][1]
    i = 0
    while i < (len(line_log)-len(line_log[second_header[1]])):
        #pattern matching
        current_line = line_log[second_header[1]-i]
        prefixmatches = re.search(prefix,str(current_line)) is not None
        #llprefixmatches = re.search(prefix,lastline) is not None
        suffixmatches = re.search(suffix,str(current_line)) is not None
        for word in result_options:
            matches = re.search(word,str(current_line)) is not None
            if(prefixmatches and matches and suffixmatches):
                partial = re.search("(partially(.*))+ "+word+"|"+word+"(.*)(in part)+",str(current_line)) is not None
                if(partial):
                    results.append(result_options.index(word)+5)
                else:
                    results.append(result_options.index(word))
            
            
        i += 1
    
    if(len(results) == 0): results = [4]
    return list(set(results))
    
#print(extract_result(path))
