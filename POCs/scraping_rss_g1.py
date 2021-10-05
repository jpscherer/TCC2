import requests
from bs4 import BeautifulSoup

page = requests.get("https://g1.globo.com/rss/g1/politica/")

soup = BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())
#print(soup.children)

xml = list(soup.children)[2]

noticias = list(soup.find_all('item'))

primeira_noticia = list(noticias)[0]
titulo_noticia = primeira_noticia.find_all('title')
descricao_noticia = primeira_noticia.find_all('description')

print('Notícia 1: ')
print(titulo_noticia)
print(descricao_noticia)

