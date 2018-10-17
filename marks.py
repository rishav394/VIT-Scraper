import index
import re
import json
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
if index.error == "":
    url = "https://vtopbeta.vit.ac.in/vtop/examinations/doStudentMarkView"
    data = {'semesterSubId': index.semester}
    url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
    soup = BeautifulSoup(url.content, 'html.parser')
    table = soup.find_all('table')
    final_mark = []
    final_mark1 = {}
    if len(table) > 0:
        tr = table[0].find_all('tr')
        for i in range(1, len(tr)):
            if tr[i - 1].has_attr('style'):
                if tr[i - 1]['style'] == 'background-color: #d2edf7;':
                    course_info = tr[i - 1].find_all('td')
                    marks = {
                        'class_no': course_info[1].text,
                        'code': course_info[2].text,
                        'title': course_info[3].text,
                        'type': course_info[4].text,
                        'credit': course_info[5].text,
                        'faculty': course_info[7].text,
                        'slot': course_info[8].text
                    }
                    mark_info = tr[i].find_all('td')[0].find_all('table')[0]
                    mark_tr = mark_info.find_all('tr')
                    store_mark = []
                    for j in range(1, len(mark_tr)):
                        td1 = mark_tr[j].find_all('td')
                        mark_sub = {
                            'title': td1[1].find_all('output')[0].text,
                            'max': td1[2].find_all('output')[0].text,
                            'weightage': td1[3].find_all('output')[0].text,
                            'status': td1[4].find_all('output')[0].text,
                            'scored': td1[5].find_all('output')[0].text,
                            'percentage': td1[6].find_all('output')[0].text
                        }
                        store_mark.append(mark_sub)
                    marks['details'] = store_mark
                    final_mark.append(marks)
        final_mark1['marks'] = final_mark
        final_mark1 = json.dumps(final_mark1)
        final_mark1 = json.loads(final_mark1)
    with open('marks.json', 'w') as outfile:
        json.dump(final_mark1, outfile, indent=41)
