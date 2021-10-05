import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.hltv.org/")

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())

html = list(soup.children)[2]
body = list(html.children)[3]

#print(body)

#today_matches = soup.find_all('todays-matches-con')[0].get_text()
today_matches = soup.find_all('todays-matches-con')#[0].get_text()
teams = soup.find_all('span', class_='team')


print('Partidas do dia')

index = 0
match = ''
for cs_team_name in teams:
    if index % 2 == 0:
        match += cs_team_name.get_text() + ' x '
    else:
        match += cs_team_name.get_text()
        print(match)
        match = ''
    index += 1

print(teams)