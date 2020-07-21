import requests
from bs4 import BeautifulSoup

url = 'https://www.lifewire.com/list-of-executable-file-extensions-2626061'
exec = []

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

extensionTable = soup.find('table', class_="mntl-sc-block-table__table")

for tb in extensionTable.find_all('tbody'):
    tr = tb.find_all('tr')
    for td in tr:
        if td.find_all('td')[2].text in ["Windows","Android"]:
            exec.append(str("."+td.find_all('td')[0].text).lower())

print(exec)
    
