import base64
import io
import sys
import warnings

import requests
from PIL import Image
from bs4 import BeautifulSoup

from CaptchaService import CaptchaParse

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
unified_session = requests.session()

username = 'your username here'
password = 'your password here'
semester = 'semester ID here'  # VL2018191 for Fall 18-19 and VL2018195 for Winter 18-19

url1 = 'https://vtop.vit.ac.in/'
unified_session.get(url1, headers=headers, verify=False)
url1 = 'https://vtop.vit.ac.in/vtop/vtopLogin'
res = unified_session.post(url1, data=None, headers=headers, verify=False)

if 'alt="vtopCaptcha"' not in res.text:
    print("Cookies error")
    sys.exit()

print("Logging in...")

soup = BeautifulSoup(res.text, 'html.parser')
image = soup.find('img', alt="vtopCaptcha")
image = (image['src'].split(" "))[1]
imgdata = base64.b64decode(image)
image = Image.open(io.BytesIO(imgdata))
captcha = CaptchaParse(image)

data = {
    'uname': username,
    'passwd': password,
    'captchaCheck': captcha
}

url1 = 'https://vtop.vit.ac.in/vtop/doLogin'
res = unified_session.post(url1, data=data, headers=headers, verify=False)
soup = BeautifulSoup(res.text, 'html.parser')
if soup.find('p', {'class': 'box-title text-danger'}) is not None:
    error = soup.find('p', {'class': 'box-title text-danger'}).text
    print(error)
    sys.exit()
print('Logged in successfully')

if res.status_code != 200:
    print("Error on VTOP's end. Yeah they suck.")
    sys.exit()
