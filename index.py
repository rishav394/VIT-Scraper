import base64
import io
import re

import warnings

import requests
from PIL import Image

from CaptchaService import CaptchaParse

from bs4 import BeautifulSoup

url1 = 'https://vtopbeta.vit.ac.in/vtop/'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
                  'Safari/537.36',
}

warnings.filterwarnings('ignore', 'Unverified HTTPS request')

reg_no = input("Enter Reg. No. ")
password = input("Enter Passwd. ")
semester = "VL2018191"
unified_session = requests.session()
url = unified_session.get(url1, headers=headers, verify=False)
regex = "gsid=[0-9]{6,7};"
pattern = re.compile(regex)
gsid = re.findall(pattern, str(url.content))
error = ""
if len(gsid) > 1:
    if len(gsid[0].split("=")) > 1:
        if len((gsid[0].split("="))[1].split(";")) > 0:
            gsid = ((gsid[0].split("="))[1].split(";"))[0]
            print("Logging in...")
            url = "https://vtopbeta.vit.ac.in/vtop/executeApp/?gsid=" + str(gsid)
            unified_session.get(url, headers=headers, verify=False)
            url = "https://vtopbeta.vit.ac.in/vtop/getLogin"
            url = unified_session.get(url, headers=headers, verify=False)
            soup = BeautifulSoup(url.content, 'html.parser')
            image = soup.find('img', alt="vtopCaptcha")
            image = (image['src'].split(" "))[1]
            imgdata = base64.b64decode(image)
            image = Image.open(io.BytesIO(imgdata))
            captcha = CaptchaParse(image)
            data = {
                'uname': reg_no,
                'passwd': password,
                'captchaCheck': captcha
            }
            url = "https://vtopbeta.vit.ac.in/vtop/processLogin"
            url = unified_session.post(url, data=data, headers=headers, verify=False)
            soup = BeautifulSoup(url.content, 'html.parser')
            if soup.find('p', {'class': 'box-title text-danger'}) is not None:
                error = soup.find('p', {'class': 'box-title text-danger'}).text
                print(error)
# print(soup.prettify())