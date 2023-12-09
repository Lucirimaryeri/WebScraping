
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import csv

url = 'https://registrar.web.baylor.edu/exams-grading/fall-2023-final-exam-schedule'
#Request in case 404 Forbidden error
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Ge-----)'}

req = Request(url, headers=headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')
print(soup.title.text) #shows that we can scrape it
print()

table = soup.findAll('table') #findall gives you a list, #find is first one that comes out
finals_table = table[1]
tr = finals_table.findAll('tr')

#opening classes file 
infile = open('myclasses.csv','r')
csv_file = csv.reader(infile)

#read through each 1 row at a time
for rec in csv_file:
    myclass = rec[0]
    mytime = rec[1]

    for row in tr: #findall gives you an iterable object, find gives you just one instance -- find in hw assignment 
        td = row.findAll("td")
        if td:
            sch_class = td[0].text
            sch_time = td[1].text
            exam_day = td[2].text
            exam_time = td[3].text

            if sch_class == myclass and sch_time == mytime:
                print(myclass,mytime,exam_day,exam_time)

               # 1st part -- midterm list comp-webscraping pt 2-- webscraping and excel (opennote)

print()

            

