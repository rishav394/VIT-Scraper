import json
import re
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

# TODO: Update for new VTOP

if index.error == "":
    url = "https://vtop.vit.ac.in/vtop/examinations/doDigitalAssignment"
    data = {
        'semesterSubId': index.semester
    }

    url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
    soup = BeaL̥utifulSoup(url.content, 'html.parser')
    table = soup.find_all('table')[0]
    tr = table.find_all('tr')
    length = len(tr)
    assignment1 = []
    final_assignment = {}
    if length > 1:
        for i in range(1, length):
            assignment = {}
            tr1 = tr[i]
            td = tr1.find_all('td')
            assignment['class_no'] = td[1].text
            assignment['code'] = td[2].find_all('p')[0].text
            assignment['title'] = td[3].find_all('p')[0].text
            assignment['type'] = td[4].text
            assignment['slot'] = td[11].text
            assignment['faculty'] = td[12].find_all('p')[0].text
            assignment['option'] = td[10].text
            data = {
                'classId': td[1].text,
                'courseCode': td[2].find_all('p')[0].text,
                'title': td[3].find_all('p')[0].text,
                'type': td[4].text,
                'option': td[10].text,
                'slot': td[11].text,
                'fName': td[12].find_all('p')[0].text
            }
            url = "https://vtop.vit.ac.in/vtop/examinations/processDigitalAssignment"
            url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
            soup1 = BeautifulSoup(url.content, 'html.parser')
            table1 = soup1.find_all('table')[1]
            tr2 = table1.find_all('tr')
            length1 = len(tr2)
            details = []
            if length1 > 1:
                for j in range(1, length1):
                    assignment_detail = {}
                    tr3 = tr2[j]
                    td1 = tr3.find_all('td')
                    assignment_detail['title'] = td1[1].text
                    assignment_detail['max'] = td1[2].text
                    assignment_detail['weightage'] = td1[3].text
                    assignment_detail['due_date'] = td1[4].find_all('span')[0].text
                    chk_not_upload = td1[5].find_all('span')
                    if len(chk_not_upload) == 2:
                        if len(chk_not_upload[0].text) == 1:
                            s = chk_not_upload[1].text
                            s = re.sub('\s+', ' ', s)
                        else:
                            s = 'Not uploaded'
                    else:
                        s = '-'
                    assignment_detail['status'] = s
                    details.append(assignment_detail)
            assignment['details'] = details
            assignment1.append(assignment)
        final_assignment['assignment'] = assignment1
        final_assignment = json.dumps(final_assignment)
        final_assignment = json.loads(final_assignment)
    with open('assignments.json', 'w') as outfile:
        json.dump(final_assignment, outfile, indent=4)
