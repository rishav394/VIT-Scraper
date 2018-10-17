import json
import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
if index.error == "":
    url = "https://vtopbeta.vit.ac.in/vtop/processViewTimeTable"
    data = {
        'semesterSubId': index.semester
    }
    url = index.unified_session.post(url, data=data, headers=index.headers, verify=False)
    soup = BeautifulSoup(url.content, 'html.parser')
    table = soup.find_all('table')[0]
    length = len(table.find_all('tr'))
    timetable1 = {}  # array
    timetable = []  # list
    # 0 is bullshit
    # 1 is heading
    # last 2 is bullshit again
    for i in range(2, length - 2):
        course = {}  # array
        tr = table.find_all('tr')[i]
        td = tr.find_all('td')
        course['code'] = td[2].find_all('p')[0].text
        course['title'] = td[3].find_all('p')[0].text
        course['type'] = td[4].find_all('p')[0].text
        course['credit'] = td[5].find_all('p')[0].text
        course['class_no'] = td[7].find_all('p')[0].text
        course['slot'] = td[8].find_all('p')[0].text
        course['venue'] = td[9].find_all('p')[0].text
        course['faculty'] = td[10].find_all('p')[0].text
        timetable.append(course)  # add array (course) to list (timetable)
    timetable1['Timetable'] = timetable  # add the element<List<Arrays>> (timetable list) in the array
    timetable1 = json.dumps(timetable1)
    timetable1 = json.loads(timetable1)
    with open('course_details.json', 'w') as outfile:
        json.dump(timetable1, outfile, indent=4)
