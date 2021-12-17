from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams
import os
import re


def process_document(title,response):
    
    counter = 0
    file = open(str(counter)+".pdf", 'wb').write(response.content)
    print(title + str(extract_result(str(counter)+".pdf")))
    
    #uncomment the line above to store all files


def extract_result(path):
    result_options = [r"affirmed",r"remanded",r"vacate",r"reversed"]
    
    prefix = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)"
    whole = r"[0-9]+ F. [0-9]{0,1}d [0-9]+,(.*)\.( )*$"
    suffix = r"^(.*)\.(.*)$"
    end_of_syllabus = r"Opinion(.*)\."

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
                results.append(result_options.index(word))
            
        i += 1
    
    return results
    
#print(extract_result(path))
