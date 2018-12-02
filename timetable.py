import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
url = "https://vtop.vit.ac.in/vtop/processViewTimeTable"
data = {
    'semesterSubId': index.semester
}
url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
table = soup.find_all('table')[1]
length = len(table.find_all('tr'))
timetable1 = {}  # array
timetable = []  # list
for i in range(4, length):
    course = {}
    tr = table.find_all('tr')[i]
    td = tr.find_all('td', rowspan=None)
    print(td)
    # for later
