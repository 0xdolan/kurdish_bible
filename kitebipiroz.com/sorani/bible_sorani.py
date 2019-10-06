import requests
from bs4 import BeautifulSoup

url = requests.get('http://www.kitebipiroz.com/bible').text
soup = BeautifulSoup(url, 'lxml')

links = []
for link in soup.find_all('table'):
    for tr in link.find_all('a'):
        links.append('http://www.kitebipiroz.com' + tr['href'])

for each in links:
    print(each)
    complete_url = requests.get(each).text
    soup1 = BeautifulSoup(complete_url, 'lxml')
    for text in soup1.find_all('div', id="main-content-inner"):
##        print(text.text)
        with open('bible_sorani.txt', 'a', encoding='utf-8') as f:
            f.write(str(text.text))
