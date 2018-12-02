import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import student_details


def main(tono, todata):
    gmail_user = 'gmailacount@gmail.com'
    gmail_password = 'yourpassword'

    to = tono

    subject = 'Your assignment dates'

    msg = MIMEText(todata)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, msg.as_string())
        server.quit()

        print('Email sent!')

    except:
        print('Something went wrong...')


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
                    a = a + (str(title) + "'s " + y['title'] + "\n\t\tdue on " + str(due) + "\n")
    a = a.strip("\n\r")
    print(a)
    print(len(a))
    main(str(student_details.email()), a)
