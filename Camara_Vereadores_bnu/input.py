import nltk
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
import pandas as pd
import output
import codecs
import categoria_helper
from datetime import datetime

# Posteriormente remover
default_page_url = "https://digital.camarablu.sc.gov.br/documentos/tipo:projetos-2/subtipo:103%2C105%2C106%2C102%2C104/numero:/numero_final:/ano:/ordem:Documento.data%20DESC/autor:/assunto:/processo:/documento_data_inicial:/documento_data_final:/publicacoes-legais:/situacao:/termo:/operadorTermo2:AND/termo2:/protocolo:"
url_base = "https://digital.camarablu.sc.gov.br"
caminho_padrao_armazenamento_pagina = '';
filtro_data = datetime.strptime('01/10/2021', '%d/%m/%Y')
default_page_path = ''
processar_categorias = False;
utilizar_paginas_salvas = False;
filtro_atendido = False;

data_inicio_filtro, data_fim_filtro = datetime.strptime('01/10/2021', '%d/%m/%Y')
# Posteriormente remover

def dataframe_gerador(data):
    return pd.DataFrame(data, columns = ['Projetos', 'Autores', 'Data', 'Categorias'])

##################################### #####################################

def get_soup_pagina(project_href):
    primeiro_index = project_href.find('/', 1)
    nome_arquivo = project_href[primeiro_index + 1: len(project_href)]
    nome_arquivo_completo = caminho_padrao_armazenamento_pagina + '/' + nome_arquivo + '.html'

    if (utilizar_paginas_salvas):
        #Quando por arquivo .html
        f = codecs.open(nome_arquivo_completo, "r", "utf-8")
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup;
    else:
        page = requests.get(url_base + project_href, timeout=120)
        soup = BeautifulSoup(page.content, 'html.parser')
        output.salvar_html_pagina(nome_arquivo_completo, soup);
        return soup;

##################################### #####################################

def get_project_info(project_href):
    soup = get_soup_pagina(project_href)
    itens_projeto = list(soup.find_all('li', class_='documento-item'))

    item_data = itens_projeto[0]
    str_data = item_data.findChildren('div', class_='col-xs-8 col-sm-10')[0].text.rstrip().lstrip();
    data_projeto = datetime.strptime(str_data, '%d/%m/%Y')

    item_autor = itens_projeto[1]
    nome_autors = item_autor.findChildren('div', class_='col-xs-8 col-sm-10');

    formated_autor_names = []
    [formated_autor_names.append(item.text.rstrip().lstrip().replace('\n', '-')) for item in nome_autors]

    return formated_autor_names[0], data_projeto;

##################################### #####################################

def scrap_projects_page(page_url):
    if page_url == 0:
        return

    #Quando via requisição
    page = requests.get(page_url, timeout=120)
    soup = BeautifulSoup(page.content, 'html.parser')

    projetos = soup.find_all('a', class_='list-link') # clearfixcol-xs-12 col-sm-7

    lista_projetos = []
    lista_autores = []
    lista_datas = []
    lista_categorias = []

    for item in list(projetos):
        href_projeto = item.get('href')
        title_element = item.findChildren('p')[0]

        title = title_element.text.rstrip().lstrip()
        (autores_projeto, data_projeto) = get_project_info(href_projeto);

        if ((data_fim_filtro != 0 and data_fim_filtro.month < data_projeto.month and data_fim_filtro.year < data_projeto.year) or
            (data_inicio_filtro.month > data_projeto.month and data_inicio_filtro.year > data_projeto.year)):
            global filtro_atendido
            filtro_atendido = True
            break

        autor = ''.join(autores_projeto)

        lista_projetos.append(title)
        lista_autores.append(autor)
        lista_datas.append(data_projeto)
        lista_categorias.append(categoria_helper.processa_categoria(title, educacao_palavras, seguranca_palavras, saude_palavras, infra_palavras, economia_palavras))

        print('.', end = '')

    data =  { 'Projetos' : lista_projetos,
              'Autores': lista_autores,
              'Data': lista_datas,
              'Categorias': lista_categorias
            }

    return pd.DataFrame(data, columns = ['Projetos', 'Autores', 'Data', 'Categorias']);
##################################### #####################################

def popular_dataframes(data_inicio, data_fim):

    df = dataframe_gerador([]);
    filtro_atendido = False;
    page_number = 1

    while (filtro_atendido == False):
        page_url = default_page_url;
        if page_number > 1:
            page_url += "/page:" + str(page_number)

        df_projeto = dataframe_gerador(scrap_projects_page(page_url));

        df = df.append(df_projeto)
        page_number += 1

    return 0;


popular_dataframes(0, 0);