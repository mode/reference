import shutil
import glob
import os
from os.path import basename
import requests
import urllib2
import urllib
import csv
import zipfile
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag

## File for examples this XLS file
# http://www.bls.gov/soc/soc_2010_direct_match_title_file.xls

def write_to_csv(csv_name,array):
    columns = len(array[0])
    rows = len(array)
    
    with open(csv_name, "wb") as test_file:
        file_writer = csv.writer(test_file)
        for i in range(rows):
            file_writer.writerow([array[i][j] for j in range(columns)])


## Get site data
print "Going to bls.gov..."
url = "http://www.bls.gov/oes/current/oes_stru.htm"
r = requests.get(url)
soup = BeautifulSoup(r.text)


## Loop through lists
print "Finding occupations..."
result = []
header = ('major_group_code','major_group_name','minor_group_code','minor_group_name',
    'broad_group_code','broad_group_name','occupation_code','occupation_name')
result.append(header)

headers = soup.findAll("h3")

for h in headers:
    header_link = h.find("a")
    header_sibling = header_link.nextSibling
    
    if header_sibling is not None:
        major_group_code = header_link.text.strip()
        major_group_name = header_sibling.strip()
        
        if major_group_code != '00-0000':
            
            minor_group_ul = h.findNext("ul")
            minor_groups = minor_group_ul.findAll("li",recursive=False)
            
            for mg in minor_groups:
                minor_group_code = mg.text[:7].strip()
                minor_group_name = mg.text[7:].strip()
                
                broad_group_ul = mg.findNext("ul")
                broad_groups = broad_group_ul.findAll("li",recursive=False)
                
                for bg in broad_groups:
                    broad_group_code = bg.text[:7].strip()
                    broad_group_name = bg.text[7:].strip()
                    
                    occupation_ul = bg.findNext("ul")
                    occupations = occupation_ul.findAll("li",recursive=False)
                    
                    for oc in occupations:
                        occupation_code = oc.text[:7].strip()
                        occupation_name = oc.text[7:].strip()
                        
                        entry = (major_group_code,major_group_name,minor_group_code,minor_group_name,
                                    broad_group_code,broad_group_name,occupation_code,occupation_name)
                        
                        result.append(entry)
            
## Output to CSV
write_to_csv("bls_occupation_codes.csv",result)