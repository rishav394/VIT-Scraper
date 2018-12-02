import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

url = "https://vtop.vit.ac.in/vtop/examinations/examGradeView/StudentGradeHistory"
data = {
    "verifyMenu": "true",
    "winImage": "undefined",
    "authorizedID": index.username,
    "nocache": "@(new Date().getTime())"
}
url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
table = soup.find_all('table', {"class": "customTable"})[1]
trs = table.find_all('tr', {"style": None})
heading = trs[1].find_all('td')
heading = heading[0:-1]
trs = trs[2:]
final = []
for i in range(0, len(trs)):
    subject = {}
    tds = trs[i].find_all('td')
    tds = tds[0:-1]
    for j in range(0, len(tds)):
        subject[heading[j].text] = tds[j].text
    final.append(subject)

final = json.dumps(final)
final = json.loads(final)
with open('grade_history.json', 'w') as outfile:
    json.dump(final, outfile, indent=4)
