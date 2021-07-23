import requests
from bs4 import BeautifulSoup

# (not very important) these data provide web server with our device information. (though some website may check this part)
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

CRAWL_URL = 'https://web.ee.ntu.edu.tw/'

session = requests.Session()
session.headers = {'user-agent' : USER_AGENT}

req = session.get(CRAWL_URL)

soup = BeautifulSoup(req.text, 'html.parser')

element_honor_box = soup.find_all(class_="honor_box")[0]

honor_title = element_honor_box.find_all(class_="honor_title")
honor_content = element_honor_box.find_all(class_="honor_content")
for h in honor_content:
    # remove child element
    element_a = h.find('a')
    element_a.decompose()

print("榮譽榜")
for i in range(len(honor_content)):
    print("{} - {}".format(honor_title[i].string,honor_content[i].string))
