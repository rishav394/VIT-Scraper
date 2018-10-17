import json
import re
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

if index.error == "":
    url = "https://vtopbeta.vit.ac.in/vtop/studentsRecord/StudentProfileAllView"
    data = {
        'semesterSubId': index.semester
    }
    url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
    soup = BeautifulSoup(url.content, 'html.parser')
    table = soup.find_all('table')[0]
    tr = table.find_all('tr')
    length = len(tr)
    data = {}
    if length > 1:
        for i in range(1, length):
            td = tr[i].findAll('td')
            if len(td) > 1:
                data[str(td[0].text).replace("\n", ' ').replace('\t', '')] = td[1].text
    final_assignment = {'Student_Details': data}
    final_assignment = json.dumps(final_assignment)
    final_assignment = json.loads(final_assignment)
    with open('student_details.json', 'w') as outfile:
        json.dump(final_assignment, outfile, indent=4)


def email():
    return final_assignment['Student_Details']['Email']
