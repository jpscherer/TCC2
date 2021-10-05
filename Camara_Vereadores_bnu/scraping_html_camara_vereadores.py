import nltk
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
import pandas as pd
import output
import codecs

st = nltk.stem.RSLPStemmer()
stopwords = set(nltk.corpus.stopwords.words('portuguese'))

educacao_palavras = [st.stem('escola'), st.stem('laboratório'), st.stem('educação'), st.stem('informática')]
seguranca_palavras = [st.stem('policial'),st.stem('assalto'), st.stem('roubo')]
saude_palavras = [st.stem('vacinação')]
infra_palavras = [st.stem('prolongamento'), st.stem('via'), st.stem('praça')]
economia_palavras = [st.stem('orçamento'), st.stem('financeiro'), st.stem('fundos'), st.stem('créditos'), st.stem('pagamentos'), st.stem('auxílio')]

caminho_padrao_armazenamento_pagina = 'D:/TCC2/Paginas';

url_base = "https://digital.camarablu.sc.gov.br"

def remove_stopwords(expressao):
    palavras = [i for i in expressao.split() if not i in stopwords]
    return (" ".join(palavras))

#titulo_projeto: string
#nome_autor: string[]
def processa_categoria(titulo_projeto, nome_autor):
    categorias_projetos = []
    titulo_projeto = remove_stopwords(titulo_projeto.lower())

    # for verificando palavras educacao
    for palavra_educacao in educacao_palavras:
        if titulo_projeto.count(palavra_educacao) > 0:
            categorias_projetos.append('Educação')

    # for verificando palavras segurança
    for palavra_seguranca in seguranca_palavras:
        if titulo_projeto.count(palavra_seguranca) > 0:
            categorias_projetos.append('Segurança')

    # for verificando palavras saúde
    for palavra_saude in saude_palavras:
        if titulo_projeto.count(palavra_saude) > 0:
            categorias_projetos.append('Saúde')

    # for verificando palavras infraestrutura
    for palavra_infra in infra_palavras:
        if titulo_projeto.count(palavra_infra) > 0:
            categorias_projetos.append('Infra')

    # for verificando palavras economia
    for palavra_economia in economia_palavras:
        if titulo_projeto.count(palavra_economia) > 0:
            categorias_projetos.append('Economia')

    #Para realizar o distinct
    categorias_projetos = list(set(categorias_projetos))

    return categorias_projetos

def get_next_page_url(soup):
    li_next_pag = soup.find_all('li', class_='next-pag')
    href_next_page = list(li_next_pag[0].children)[0].get('href')

    page = requests.get(url_base + href_next_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_next_page_url(soup)

    #return url_base + href_next_page
    #return 0

def get_quantidade_projetos_categoria(df_autor, categoria):
    mask_filter_categoria = df_autor.Categorias.apply(lambda x: categoria in x)
    return len(df_autor[mask_filter_categoria].index)

def get_autor_names(project_href):
    primeiro_index = project_href.find('/', 1)
    nome_arquivo = project_href[primeiro_index + 1: len(project_href)]
    nome_arquivo_completo = caminho_padrao_armazenamento_pagina + '/' + nome_arquivo + '.html'

    # Quando por arquivo .html
    # f = codecs.open(nome_arquivo_completo, "r", "utf-8")
    # content = f.read()
    # soup = BeautifulSoup(content, 'html.parser')

    page = requests.get(url_base + project_href)
    soup = BeautifulSoup(page.content, 'html.parser')

    output.salvar_html_pagina(nome_arquivo_completo, soup);

    item_autor = list(soup.find_all('li', class_='documento-item'))[1]
    nome_autors = item_autor.findChildren('div', class_='col-xs-8 col-sm-10');

    formated_autor_names = []
    [formated_autor_names.append(item.text.rstrip().lstrip().replace('\n', '-')) for item in nome_autors]
    return formated_autor_names[0];

##################################### Captura títulos dos projetos #####################################
def scrap_projects_page(page_url):
    if page_url == 0:
        return

    #Quando por arquivo .html
    # page_url = "D:\TCC2\Paginas\principal.html";
    # f = codecs.open(page_url, "r", "utf-8")
    # content = f.read()
    # soup = BeautifulSoup(content, 'html.parser')

    #Quando via requisição
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    output.salvar_html_pagina(caminho_padrao_armazenamento_pagina + '/principal.html', soup);

    projetos = soup.find_all('a', class_='list-link') # clearfixcol-xs-12 col-sm-7

    lista_projetos = []
    lista_autores = []
    lista_categorias = []

    for item in list(projetos):
        href_projeto = item.get('href')
        title_element = item.findChildren('p')[0]

        title = title_element.text.rstrip().lstrip()
        autor = ''.join(get_autor_names(href_projeto))
        # autor = 'teste';

        lista_projetos.append(title)
        lista_autores.append(autor)
        lista_categorias.append(processa_categoria(title, autor))

        print('.', end = '')

    data =  { 'Projetos' : lista_projetos,
              'Autores': lista_autores,
              'Categorias': lista_categorias
            }

    return pd.DataFrame(data, columns = ['Projetos', 'Autores', 'Categorias']);
##################################### Captura títulos dos projetos #####################################


##################################### Captura quantidade páginas definidas pelo usuário #####################################
page_number = 0
total_pages = 1#int(input("Quantas páginas buscar? "))
autor = 'Poder Executivo'
default_page_url = "https://digital.camarablu.sc.gov.br/documentos/tipo:projetos-2/subtipo:103%2C105%2C106%2C102%2C104/numero:/numero_final:/ano:/ordem:Documento.data%20DESC/autor:/assunto:/processo:/documento_data_inicial:/documento_data_final:/publicacoes-legais:/situacao:/termo:/operadorTermo2:AND/termo2:/protocolo:"
#default_page_url = "D:\TCC2\Paginas\principal.html"

def dataframe_gerador(data):
    return pd.DataFrame(data, columns = ['Projetos', 'Autores', 'Categorias'])

df = dataframe_gerador([]);

while page_number < total_pages:
    if page_number > 1:
        default_page_url += "/page:" + str(page_number)

    #df = df.append(pd.DataFrame(scrap_projects_page(default_page_url), columns = ['Projetos', 'Autores', 'Categorias']))
    df = df.append(dataframe_gerador(scrap_projects_page(default_page_url)))

    output.printar_console(df);
    output.exportar_csv(df);

    page_number += 1

print('Autor: ' + autor)
df_autor = df.query('Autores == "' + autor + '"')
print(df_autor)

qtd_educacao = get_quantidade_projetos_categoria(df_autor, 'Educação')
qtd_seguranca = get_quantidade_projetos_categoria(df_autor, 'Segurança')
qtd_saude = get_quantidade_projetos_categoria(df_autor, 'Saúde')
qtd_infra = get_quantidade_projetos_categoria(df_autor, 'Infra')
qtd_economia = get_quantidade_projetos_categoria(df_autor, 'Economia')

print('Educação: ' + str(qtd_educacao))
print('Segurança: ' + str(qtd_seguranca))
print('Saúde: ' + str(qtd_saude))
print('Infra: ' + str(qtd_infra))
print('Economia: ' + str(qtd_economia))

output.gerar_grafico_estrela(autor, qtd_educacao, qtd_seguranca, qtd_saude, qtd_infra, qtd_economia)

##################################### Captura quantidade páginas definidas pelo usuário #####################################
