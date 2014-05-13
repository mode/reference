import re
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

def write_to_csv(csv_name,array):
    columns = len(array[0])
    rows = len(array)
    
    with open(csv_name, "wb") as test_file:
        file_writer = csv.writer(test_file)
        for i in range(rows):
            file_writer.writerow([array[i][j] for j in range(columns)])

def strip_special(array,columns_with_string):
    new_table = []
    for i in array:
        new_row =[]
        for j in range(len(i)):
            if j in columns_with_string:
                x = i[j].encode('utf-8').strip()
            else:
                x = i[j]
            new_row.append(x)
            
        new_table.append(new_row)
    
    return new_table

## Get site data
print "Going to qppstudio.net..."
url = "http://www.qppstudio.net/publicholidays.htm"
r = requests.get(url)
soup = BeautifulSoup(r.text)

## Get link list
print "Getting country links"
country_links = []
all_links = soup.findAll('a')
for idx,l in enumerate(all_links):
    try:
        tle = l['title']
        if tle.index('2014 Calendar of Legal holidays') == 0:
            country_links.append(l)
    except:
        None

## Loop through countries
print "Looping through countries..."

full_list = []
header = (['country','holiday_date','day_of_week','holiday','partially_celebrated','notes'])
full_list.append(header)

errors = []

for c in country_links:
    
    country = c.text
    print "Getting %s..." % country
    
    href = c['href']
    url_2014 = "http://www.qppstudio.net/" + href
    url_2015 = url_2014.replace('2014','2015')
    
    list_2014 = get_holidays(url_2014,country,2014)
    list_2015 = get_holidays(url_2015,country,2015)
    
    full_list = full_list + list_2014[0] + list_2015[0]
    errors = errors = list_2014[1] + list_2015[1]

clean_list = strip_special(full_list,(0,3))
write_to_csv("holidays.csv",clean_list)

def get_holidays(url,country,year):
    results = []
    error_table = []
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    
    cells = soup.findAll('td')
    
    for c in cells:
        contents = c.text
        
        if "unescape(" in contents and "obCkDate" not in contents:
            
            try:
                ## Check if it's a date
                unescape_position = contents.index("unescape(")
                end_position = contents.index("))")
                
                ## Check if it's a regional/partially celebrated holiday
                if c.text.strip()[-1] == "*":
                    partial = True
                else:
                    partial = False
                
                ## Get date
                string = contents[unescape_position + len("unescape(") + 1:end_position - 1]
                date = get_date(string)
                
                day_position = re.search("\d", date).start()
                
                if day_position != 0:
                    month = date[:day_position].strip()
                
                day = date[day_position:]
                
                holiday_date = "%s-%s-%s" % (year,month,day)
                
                ## Get day
                day_cell = c.findNext("td")
                day = day_cell.text.strip()
                
                ## Get holiday
                holiday_cell = day_cell.findNext("td")
                holiday = holiday_cell.text.strip()
                
                ## Get notes
                note_cell = holiday_cell.findNext("td")
                note = note_cell.text.strip()
                
                entry = (country,holiday_date,day,holiday,partial,note)
                results.append(entry)
                
            except Exception as e:
                print e
                print "There was an error for the %s holidays in %s" % (year,country)
                error_entry = (country,year,url)
                error_table.append(error_entry)
    
    return [results,error_table]

def get_date(string):
    uncoded = urllib.unquote(string)
    date = uncoded[len("<!--HPSTART-->"):-len("<!--HPEND-->")]
    
    if "<" in date:
        start_el = date.index("<")
        end_el = date.index(" ")
        el_length = end_el - start_el
        remove_close = date[:-(el_length + 2)]
        
        start_el_close = date.index(">")
        date = remove_close[start_el_close + 1:]
    
    old_length = len(date)
    new_length = 0
    
    while new_length != old_length:
        old_length = len(date)
        date = date.replace("&nbsp;&nbsp;","&nbsp;")
        new_length = len(date)
    
    drop_period = date.replace(".","")
    finished_date = drop_period.replace("&nbsp;"," ").strip()
    return finished_date



for idx,c in enumerate(cells):
    if "unescape(" in c.text:
        print idx