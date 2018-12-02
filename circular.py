import warnings

from bs4 import BeautifulSoup

import index

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
url = "https://vtop.vit.ac.in/vtop/admissions/costCentreCircularsViewPageController"
url = index.unified_session.post(url, headers=index.headers, verify=False)
soup = BeautifulSoup(url.content, 'html.parser')
a = soup.find_all('a')
# current path
path = os.path.dirname(os.path.realpath(__file__))
circular_dir = "circular"
for i in range(len(a)):
    text = a[i].text.split(".")[0]
    x = (a[i]['onclick']).split("(")
    x = x[1].split(")")[0].split("'")
    url = "https://vtop.vit.ac.in/vtop/admissions/viewStatusWiseCostCentreCircularContent?val=" + x[1]
    url = index.unified_session.get(url, headers=index.headers, verify=False)
    content = (url.headers['Content-Type']).split("/")[1]
    if not os.path.exists(os.path.join(path, circular_dir)):
        os.makedirs(os.path.join(path, circular_dir))
    filePath = os.path.join(path, circular_dir, x[1] + '.' + content)
    if not os.path.exists(filePath):
        with open(filePath, 'wb') as f:
            f.write(url.content)
