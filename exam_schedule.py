import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

url = "https://vtop.vit.ac.in/vtop/examinations/doSearchExamScheduleForStudent"
data = {
    "authorizedID": index.username,
    "semesterSubId": index.semester
}
req = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(req.content, 'html.parser')
table = soup.find_all('table', {"class": "customTable"})[0]
headings = (table.find('tr')).find_all('td')
trs = table.find_all('tr')
trs = trs[1:]
i = 0
exam = {}
while i < len(trs):
    tds = trs[i].find_all('td')
    if len(tds) == 1:
        exam_type = tds[0].text
        each_exam = []
        i = i + 1
        tds = trs[i].find_all('td')
        while len(tds) > 1:
            each_sub = {}
            for j in range(0, len(tds)):
                each_sub[headings[j].text] = tds[j].text
            each_exam.append(each_sub)
            i = i + 1
            if i < len(trs):
                tds = trs[i].find_all('td')
            else:
                break
        exam[exam_type] = each_exam
    else:
        i = i + 1
exam = json.dumps(exam)
exam = json.loads(exam)
with open('exam_schedule.json', 'w') as outfile:
    json.dump(exam, outfile, indent=4)
