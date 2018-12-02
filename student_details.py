import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

url = "https://vtop.vit.ac.in/vtop/studentsRecord/StudentProfileAllView"
data = {
    "verifyMenu": "true",
    "winImage": "undefined",
    "authorizedID": index.username,
    "nocache": "@(new Date().getTime())"
}
url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')

final = {}

table = soup.findAll('table')
rows = []
for i in range(0, len(table)):
    trs = table[i].find_all('tr')
    for j in range(0, len(trs)):
        rows.append(trs[j])

i = 0
tr = rows
blocks = {}
while True:
    td = tr[i].find_all('td')
    mytext = td[0].text
    i += 1
    td = tr[i].find_all('td')
    block = {}
    while len(td) != 1:
        block[td[0].text.replace('\t', '').replace('\r', '').replace('\n', ' ').strip()] = td[1].text
        i += 1
        if i >= len(tr):
            break
        td = tr[i].find_all('td')
    blocks[mytext.replace('\t', '').replace('\r', '').replace('\n', ' ')] = block
    if i >= len(tr):
        break

blocks = json.dumps(blocks)
blocks = json.loads(blocks)
with open('student_details.json', 'w') as outfile:
    json.dump(blocks, outfile, indent=4)

# Email return
