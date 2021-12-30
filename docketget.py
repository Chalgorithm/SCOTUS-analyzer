import os
import re
import pdfplumber as plumber


global troublemakers
troublemakers = []

def scan_for_docket_number(filename):
    print("reading: "+filename+"...")
    root = 'C:\\Users\\cjhal\\OneDrive\\Documents\\SCB\\data'
   
    is_textfile = re.match(r"(.)*\.txt$",filename) is not None
    is_pdffile = re.match(r"(.)*\.pdf$",filename) is not None
    
    if is_textfile:
        brieffile = open(str(root)+"\\"+str(filename),'r',encoding="utf-8")
        for word in brieffile.read().split():
            docket_number = re.match(r"([0-9]{2}-(.)*)",word)
            if(docket_number is not None):
                return docket_number.group(1)
    elif is_pdffile:
        try:
            pdf = plumber.open(str(root)+"\\"+str(filename))
            first_page_text = pdf.pages[0].extract_text()
            for word in first_page_text.split():
                docket_number = re.match(r"([0-9]{2}-(.)*)",word)
                if(docket_number is not None):
                    return docket_number.group(1)
        except plumber.pdfminer.pdfparser.PDFSyntaxError as pe:
            troublemakers.append(filename)
    else:
        troublemakers.append(filename)




if __name__ == "__main__":
    files = os.listdir('C:\\Users\\cjhal\\OneDrive\\Documents\\SCB\\data')
    mapping = {}
    
    for fname in files:
        
        mapping[fname] = scan_for_docket_number(fname)
        print("finished: "+str(fname)+"docket:"+str(mapping[fname]))
    
    #print(str(files[0])+":"+str(scan_for_docket_number(files[0])))
    #print(mapping)
    print("could not read the following "+str(len(troublemakers))+" files:")
    for index,troublemaker in enumerate(troublemakers):
        print(str(index)+" -> "+troublemaker)