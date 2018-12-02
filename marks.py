import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

url = "https://vtop.vit.ac.in/vtop/examinations/doStudentMarkView"
data = {
    'authorizedID': index.username,
    'semesterSubId': index.semester
}
url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
table = soup.find_all('table', {"class": "customTable"})
final_mark = []
final_mark1 = {}
if len(table) > 0:
    tr = table[0].find_all('tr', {"class": "tableContent"})
    for i in range(1, len(tr)):
        if len(tr[i].find_all('td', {"align": "center"})) == 0:  # Is a new subject
            course_info = tr[i].find_all('td')
            marks = {
                'class_no': course_info[1].text,
                'code': course_info[2].text,
                'title': course_info[3].text,
                'type': course_info[4].text,
                'credit': course_info[5].text,
                'faculty': course_info[7].text,
                'slot': course_info[8].text
            }
            i = i + 1
            details = []
            innerTable = tr[i].find('table')
            innerRows = innerTable.find_all('tr')
            for j in range(1, len(innerRows)):
                innertd = innerRows[j].find_all('td')
                each_detail = {
                    "Sl.No.": innertd[0].text,
                    "Mark Title": innertd[1].text,
                    "Max. Mark": innertd[2].text,
                    "Weightage %": innertd[3].text,
                    "Status": innertd[4].text,
                    "Scored Mark": innertd[5].text,
                    "Weightage Mark": innertd[6].text,
                    "Remark": innertd[7].text
                }
                details.append(each_detail)
            marks['details'] = details
            final_mark.append(marks)

    final_mark1['Marks'] = final_mark
    final_mark1 = json.dumps(final_mark1)
    final_mark1 = json.loads(final_mark1)
    with open('marks.json', 'w') as outfile:
        json.dump(final_mark1, outfile, indent=4)
