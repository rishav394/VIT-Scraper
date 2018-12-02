import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

url = "https://vtop.vit.ac.in/vtop/processViewStudentAttendance"
data = {
    "semesterSubId": index.semester,
    "authorizedID": index.username,
    "x": "Sun, 01 Dec 2018 12:40:04 GMT"
}
url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
table = soup.find_all('table', {"class": "table"})[0]
head = table.find_all('th')
tr = table.find_all('tr')
attendance = []
for i in range(0, len(tr)):
    tds = tr[i].find_all('td')
    each_attendance = {}
    for j in range(0, len(tds)):
        head_decode = head[j].text.replace('\n', '').replace('\r', ' ').replace('\t', '')
        text_decode = tds[j].text.replace('\n', ' ').replace('\r', '').replace('\t', '')
        each_attendance[head_decode] = text_decode
    attendance.append(each_attendance)
attendance = attendance[1:-1]
main_attendance = {'Attendance': attendance}
main_attendance = json.dumps(main_attendance)
main_attendance = json.loads(main_attendance)
with open('attendance.json', 'w') as outfile:
    json.dump(main_attendance, outfile, indent=4)
