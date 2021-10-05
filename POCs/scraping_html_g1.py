import requests
from bs4 import BeautifulSoup

page = requests.get("https://g1.globo.com/politica/noticia/2021/08/24/justica-rejeita-denuncia-do-mpf-contra-blogueiro-bolsonarista-por-ameaca-a-barroso.ghtml")

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())

html = list(soup.children)[2]
body = list(html.children)[3]

#print(body)
[print(item.text) for item in list(body.find_all('p', class_='content-text__container'))]

#print(body)

#today_matches = soup.find_all('todays-matches-con')[0].get_text()
today_matches = soup.find_all('todays-matches-con')#[0].get_text()
teams = soup.find_all('span', class_='team')
