import html_to_json
import json
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


url = "https://www.sii.cl/servicios_online/1047-nomina_inst_financieras-1714.html"
option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
driver.get(url)

time.sleep(5)
response = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(response, 'html.parser')
data = soup.find("div", class_ = "col-sm-9 contenido")

#get text
keys = []
values = []
for p in data:
    if p.find("table"):
        continue
    keys.append(p.name)
    values.append(p.get_text())

#make dict with values
text = dict(zip(keys, values))

#get table
data = soup.find(id = "tabledatasii")
table_json = html_to_json.convert_tables(str(data))

#make json file
json_file = {
        'text': text,
        'table': table_json
        }

with open('sii.json', 'w') as f:
    json.dump(json_file, f, indent=4)

driver.quit()


