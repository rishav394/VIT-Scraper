import os

from bs4 import BeautifulSoup

import index

url = "https://vtop.vit.ac.in/vtop/academics/common/StudentCoursePage"
url = index.unified_session.post(url, headers=index.headers, verify=False)
url = "https://vtop.vit.ac.in/vtop/getCourseForCoursePage"
data = {'semSubId': index.semester, 'paramReturnId': 'getCourseForCoursePage'}
url = index.unified_session.post(url, headers=index.headers, data=data, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
classId = soup.find_all('option')
if len(classId) > 1:
    for i in range(len(classId)):
        print(classId[i].text + " ", i + 1)
    print("\n")
    enter = int(input("Enter Number for course starting from 1 which has to be downloaded: "))
    for i in range(1):
        cid = classId[enter - 1]['value']
        url = "https://vtop.vit.ac.in/vtop/getSlotIdForCoursePage"
        data = {'paramReturnId': 'getSlotIdForCoursePage', 'semSubId': index.semester, 'praType': 'source',
                'classId': cid}
        url = index.unified_session.post(url, headers=index.headers, data=data, verify=False)
        soup = BeautifulSoup(url.content, 'html.parser')
        table = soup.find_all('table')[0].find_all('tr')
        path = os.path.dirname(os.path.realpath(__file__))
        coursepage = "coursepage"
        if not os.path.exists(os.path.join(path, coursepage)):
            os.makedirs(os.path.join(path, coursepage))
        if (len(table) > 2):
            for j in range(1, len(table)):
                button = table[j].find_all('button')[0]['onclick']
                button = button.split("'")
                url = "https://vtop.vit.ac.in/vtop/processViewStudentCourseDetail/?semSubId=" + button[
                    1] + "&erpId=" + button[3] + "&courseType=" + button[5] + "&roomNumber=" + button[
                          7] + "&buildingId=" + button[9] + "&slotName=" + button[11] + "&classId=" + button[
                          13] + "&courseCode=" + button[15] + "&courseTitle=" + button[17] + "&allottedProgram=" + \
                      button[19] + "&classNum=" + button[21] + "&facultyName" + button[23] + "&facultySchool=" + \
                      button[25] + "&courseId=" + button[27]
                url = index.unified_session.post(url, headers=index.headers, verify=False)
                soup = BeautifulSoup(url.content, 'html.parser')
                table0 = soup.find_all('table')[0].find_all('tr')[1].find_all('td')
                course_title = table0[1].text
                course_type = table0[2].text
                course_slot = table0[4].text
                if not os.path.exists(
                        os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                     button[23])):
                    os.makedirs(
                        os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                     button[23]))
                # table1
                table1 = soup.find_all('table')[1].find_all('tr')
                if len(table1) > 0:
                    if not os.path.exists(
                            os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                         button[23], "Reference Material")):
                        os.makedirs(
                            os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                         button[23], "Reference Material"))
                    filepath = os.path.join(path, coursepage, course_title, course_type,
                                            course_slot.replace("/", "+"), button[23], "Reference Material")
                    for k in range(len(table1)):
                        link = table1[k].find_all('td')[1].find_all('a')
                        if len(link) > 0:
                            link = "https://vtop.vit.ac.in" + link[0]['href']
                            link = index.unified_session.get(link, headers=index.headers, verify=False)
                            filename = link.headers['Content-disposition'].split(";")[1].split("=")[1]
                            filename = filename.replace("/", "+")
                            path1 = os.path.join(filepath, filename)
                            if not os.path.exists(path1):
                                try:
                                    with open(path1, 'wb') as f:
                                        f.write(link.content)
                                except IOError:
                                    print("Sorry :(")
                                    print("Downloading...")
                # table2
                a = soup.find_all('table')[2].find_all('a')
                if len(a) > 0:
                    if not os.path.exists(
                            os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                         button[23], "Lecture Material")):
                        os.makedirs(
                            os.path.join(path, coursepage, course_title, course_type, course_slot.replace("/", "+"),
                                         button[23], "Lecture Material"))
                    filepath = os.path.join(path, coursepage, course_title, course_type,
                                            course_slot.replace("/", "+"), button[23], "Lecture Material")
                    for k in range(len(a)):
                        link = "https://vtop.vit.ac.in" + a[k]['href']
                        link = index.unified_session.get(link, headers=index.headers, verify=False)
                        filename = link.headers['Content-disposition'].split(";")[1].split("=")[1]
                        filename = filename.replace("/", "+")
                        path1 = os.path.join(filepath, filename)
                        if not os.path.exists(path1):
                            try:
                                with open(path1, 'wb') as f:
                                    f.write(link.content)
                            except IOError:
                                print("Sorry :(")
                                print("Downloading...")
