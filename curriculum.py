import index
import re
import json
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore', 'Unverified HTTPS request')
if(index.error==""):
    credit={}
    url="https://vtopbeta.vit.ac.in/vtop/academics/common/Curriculum"
    data={'semesterSubId':index.semester}
    url=index.unified_session.post(url, data=data, headers=index.headers, verify=False)
    soup=BeautifulSoup(url.content,'html.parser')
    table0=soup.find_all('table')[0]
    credit1=[]
    for i in range(2,6):
        tr=table0.find_all('tr')[i]
        td1=tr.find_all('td')[1].text.replace("\n","")
        td1=td1.replace("\t"," ")
        td1=re.sub(' +',' ',td1)
        td2=tr.find_all('td')[2].text
        credit[td1]=td2
        credit1.append(credit)
    curriculum={}
    curriculum['Credits']=credit1
    for i in range(1,5):
        table=soup.find_all('table')[i]
        tr=table.find_all('tr')
        seq=[]
        for j in range(1,len(tr)):
            course={}
            td1=tr[j].find_all('td')[1].text
            td2=tr[j].find_all('td')[2].text
            td8=tr[j].find_all('td')[8].text
            course['code']=td1
            course['title']=td2
            course['credit']=td8
            seq.append(course)
        if(i==1):
            curriculum['PC']=seq
        elif(i==2):
            curriculum['PE']=seq
        elif(i==3):
            curriculum['UC']=seq
        elif(i==4):
            curriculum['UE']=seq
    curriculum=json.dumps(curriculum)
    curriculum=json.loads(curriculum)
    with open('curriculum.json','w') as outfile:
        json.dump(curriculum,outfile)
   
        
    
