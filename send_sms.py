# Use this code at your own risk
# Enter registered mobile number and password in the data dictionary
# Enter Message in data1 dictionary and enter mobile number in which message needs to be sent in toMobile in data1.

import json
from datetime import datetime

import requests


def main(tono, todata):
    url1 = 'http://www.way2sms.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    s = requests.session()
    url = s.get(url1, headers=headers, verify=False)
    data = {
        'mobileNo': 'yourMobNo',
        'password': 'way2smsPasswd',
        'CatType': ''
    }
    url = s.post('http://www.way2sms.com/re-login', data=data, headers=headers, verify=False)
    url = s.post(url1 + 'send-sms', data=data, headers=headers, verify=False)
    x = s.cookies.get_dict()['JSESSIONID']
    x = x.split('~')[1]
    data1 = {
        'Token': x,
        'message': todata,
        'toMobile': tono,
        'ssaction': 'undefined'
    }
    url = s.post(url1 + 'smstoss', data=data1, headers=headers, verify=False)


with open("assignments.json", "r") as read_file:
    a = ""
    data = json.load(read_file)
    for x in data['assignment']:
        title = x['title']
        for y in x['details']:
            if y['due_date'] != '-':
                due = datetime.strptime(y['due_date'], '%d-%b-%Y')
                due = due.date()
                now = datetime.today().date()
                if due > now:
                    a = a + (str(title).partition(' ')[0] + " - " + str(due.strftime('%d-%m-%y')) + "\n")
    a = a.strip("\n\r")
    print(a)
    print(len(a))
    main(str(9958095891), a)
