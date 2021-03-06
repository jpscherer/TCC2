import nltk
from nltk.corpus import wordnet
import requests
from bs4 import BeautifulSoup
import pandas as pd
import output
import codecs
import categoria_helper
from datetime import datetime

# Parametros Execução #
caminho_params = 'C:/Temp/params.in'

page_number = 0
total_pages = 999#int(input("Quantas páginas buscar? "))
filtro_data = datetime.strptime('01/10/2021', '%d/%m/%Y')
processar_categorias = False;
utilizar_paginas_salvas = False;
autor = ''
autor2 = ''
default_page_url = ''
default_page_path = ''
caminho_padrao_armazenamento_pagina = '';
url_base = ''
filtro_atendido = False;
popular_dataframe = False;

with open(caminho_params, "r", encoding='utf-8') as file:
    conteudo_arquivo = file.readlines();
    filtro_data = datetime.strptime(conteudo_arquivo[0].rstrip().lstrip(), '%d/%m/%Y')
    processar_categorias = conteudo_arquivo[1].rstrip().lstrip() in ['True']; #bool
    utilizar_paginas_salvas = conteudo_arquivo[2].rstrip().lstrip() in ['True']; #bool
    autor = conteudo_arquivo[3].rstrip().lstrip()
    autor2 = conteudo_arquivo[4].rstrip().lstrip()
    default_page_url = conteudo_arquivo[5].rstrip().lstrip()
    default_page_path = conteudo_arquivo[6].rstrip().lstrip()
    caminho_padrao_armazenamento_pagina = conteudo_arquivo[7].rstrip().lstrip();
    url_base = conteudo_arquivo[8].rstrip().lstrip()
    popular_dataframe = conteudo_arquivo[9].rstrip().lstrip() in ['True']; #bool

print('Filtro data: ', filtro_data)
print('Processar categorias: ', processar_categorias)
print('Utilizar páginas salvas: ', utilizar_paginas_salvas)
print('Autor1: ', autor)
print('Autor2: ',  autor2)
print('Default page url: ', default_page_url)
print('Default page path: ', default_page_path)
print('Camino padrão armazenamento pagina: ', caminho_padrao_armazenamento_pagina)
print('Url base: ', url_base)
print('Popular Dadaframe: ', popular_dataframe)

# filtro_data = datetime.strptime('01/10/2021', '%d/%m/%Y')
# processar_categorias = False;
# utilizar_paginas_salvas = False;
# autor = 'Bruno Cunha'
# autor2 = 'Poder Executivo'
# default_page_url = "https://digital.camarablu.sc.gov.br/documentos/tipo:projetos-2/subtipo:103%2C105%2C106%2C102%2C104/numero:/numero_final:/ano:/ordem:Documento.data%20DESC/autor:/assunto:/processo:/documento_data_inicial:/documento_data_final:/publicacoes-legais:/situacao:/termo:/operadorTermo2:AND/termo2:/protocolo:"
# default_page_path = "D:\TCC2\Paginas\principal.html"
# caminho_padrao_armazenamento_pagina = 'D:/TCC2/Paginas';
# url_base = "https://digital.camarablu.sc.gov.br"
# filtro_atendido = False;
# Parametros Execução #


categoria_helper.configurar(processar_categorias)

educacao_palavras = categoria_helper.gerar_palavras_educacao();
seguranca_palavras = categoria_helper.gerar_palavras_seguranca();
saude_palavras = categoria_helper.gerar_palavras_saude();
infra_palavras = categoria_helper.gerar_palavras_infra();
economia_palavras = categoria_helper.gerar_palavras_economia();
ultima_data_encontrada = datetime.strptime('31/12/2100', '%d/%m/%Y')

def get_next_page_url(soup):
    li_next_pag = soup.find_all('li', class_='next-pag')
    href_next_page = list(li_next_pag[0].children)[0].get('href')

    page = requests.get(url_base + href_next_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    get_next_page_url(soup)
    #return url_base + href_next_page
    #return 0

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


def get_quantidade_projetos_categoria(df_autor, categoria):
    mask_filter_categoria = df_autor.Categorias.apply(lambda x: categoria in x)
    return len(df_autor[mask_filter_categoria].index)

def get_project_info(project_href):
    soup = get_soup_pagina(project_href)
    itens_projeto = list(soup.find_all('li', class_='documento-item'))

    item_data = itens_projeto[0]
    str_data = item_data.findChildren('div', class_='col-xs-8 col-sm-10')[0].text.rstrip().lstrip();
    data_projeto = datetime.strptime(str_data, '%d/%m/%Y')

    if (data_projeto < filtro_data):
        global filtro_atendido
        filtro_atendido = True;

    item_autor = itens_projeto[1]
    nome_autors = item_autor.findChildren('div', class_='col-xs-8 col-sm-10');

    formated_autor_names = []
    [formated_autor_names.append(item.text.rstrip().lstrip().replace('\n', '-')) for item in nome_autors]

    # item_situacao = itens_projeto[5]
    # situacao_conteudo = item_situacao.findChildren('div', class_='col-xs-8 col-sm-10')[0].text.rstrip().lstrip();
    # data_situacao = situacao_conteudo[(len(situacao_conteudo)-10):len(situacao_conteudo)]
    # print(data_situacao)

    return formated_autor_names[0], data_projeto;

##################################### Captura títulos dos projetos #####################################
def scrap_projects_page(page_url):
    if page_url == 0:
        return

    # Quando página principal, vai mudar um pouco como capturar o nome do arquivo

    #Quando por arquivo .html
    # page_url = "D:\TCC2\Paginas\principal.html";
    # f = codecs.open(page_url, "r", "utf-8")
    # content = f.read()
    # soup = BeautifulSoup(content, 'html.parser')

    #Quando via requisição
    page = requests.get(page_url, timeout=120)
    soup = BeautifulSoup(page.content, 'html.parser')

    output.salvar_html_pagina(caminho_padrao_armazenamento_pagina + '/principal.html', soup);

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

        if (filtro_atendido == True):
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
##################################### Captura títulos dos projetos #####################################


##################################### Captura quantidade páginas definidas pelo usuário #####################################

def get_percentual_categoria(qtd_categoria, qtd_total):
    if (qtd_categoria <= 0 or qtd_total <= 0):
        return 0;

    return round(((qtd_categoria/qtd_total)*100),2)

def dataframe_gerador(data):
    return pd.DataFrame(data, columns = ['Projetos', 'Autores', 'Data', 'Categorias'])

df = dataframe_gerador([]);

page_number = 1
#while ultima_data_encontrada >= filtro_data:
if (popular_dataframe == True):
    while page_number < total_pages:
        page_url = default_page_url;
        if page_number > 1:
            page_url += "/page:" + str(page_number)

        try:
            df_pagina = dataframe_gerador(scrap_projects_page(page_url));
        except:
            print()
            print('Exceção no scrap da listagem, reprocessando página')
            print()
            continue; # se erro, não incrementa o contador da página e não adiciona ao df princípal. reprocessa a página inteira

        df = df.append(df_pagina)
        output.printar_console(df);
        output.exportar_csv(df);

        page_number += 1

        if (filtro_atendido == True):
            break

df = pd.read_csv('D:\TCC2\exportacao\projetos_camara_vereadores.csv', error_bad_lines=False);

print('Autor: ' + autor)
df_autor = df.query('Autores == "' + autor + '"')
print(df_autor)

qtd_educacao = get_quantidade_projetos_categoria(df_autor, 'Educação')
qtd_seguranca = get_quantidade_projetos_categoria(df_autor, 'Segurança')
qtd_saude = get_quantidade_projetos_categoria(df_autor, 'Saúde')
qtd_infra = get_quantidade_projetos_categoria(df_autor, 'Infra')
qtd_economia = get_quantidade_projetos_categoria(df_autor, 'Economia')
qtd_outros = get_quantidade_projetos_categoria(df_autor, 'Outros')

total_projetos_autor_periodo = qtd_educacao + qtd_seguranca + qtd_saude + qtd_infra + qtd_economia + qtd_outros

print('Educação: ' + str(qtd_educacao) + ' - ' + str(get_percentual_categoria(qtd_educacao, total_projetos_autor_periodo)) + '% no período')
print('Segurança: ' + str(qtd_seguranca) + ' - ' + str(get_percentual_categoria(qtd_seguranca, total_projetos_autor_periodo)) + '% no período')
print('Saúde: ' + str(qtd_saude) + ' - ' + str(get_percentual_categoria(qtd_saude, total_projetos_autor_periodo)) + '% no período')
print('Infra: ' + str(qtd_infra) + ' - ' + str(get_percentual_categoria(qtd_infra, total_projetos_autor_periodo)) + '% no período')
print('Economia: ' + str(qtd_economia) + ' - ' + str(get_percentual_categoria(qtd_economia, total_projetos_autor_periodo)) + '% no período')
print('Outros: ' + str(qtd_outros) + ' - ' + str(get_percentual_categoria(qtd_outros, total_projetos_autor_periodo)) + '% no período')

output.gerar_grafico_estrela2(autor, qtd_educacao, qtd_seguranca, qtd_saude, qtd_infra, qtd_economia, qtd_outros)

if (autor2 != ''):
    print('')
    print('-----------------------------------------')
    print('Autor: ' + autor2)
    df_autor2 = df.query('Autores == "' + autor2 + '"')
    print(df_autor2)

    qtd_educacao2 = get_quantidade_projetos_categoria(df_autor2, 'Educação')
    qtd_seguranca2 = get_quantidade_projetos_categoria(df_autor2, 'Segurança')
    qtd_saude2 = get_quantidade_projetos_categoria(df_autor2, 'Saúde')
    qtd_infra2 = get_quantidade_projetos_categoria(df_autor2, 'Infra')
    qtd_economia2 = get_quantidade_projetos_categoria(df_autor2, 'Economia')
    qtd_outros2 = get_quantidade_projetos_categoria(df_autor2, 'Outros')

    total_projetos_autor_periodo2 = qtd_educacao2 + qtd_seguranca2 + qtd_saude2 + qtd_infra2 + qtd_economia2 + qtd_outros2

    print('Educação: ' + str(qtd_educacao2) + ' - ' + str(get_percentual_categoria(qtd_educacao2, total_projetos_autor_periodo2)) + '% no período')
    print('Segurança: ' + str(qtd_seguranca2) + ' - ' + str(get_percentual_categoria(qtd_seguranca2, total_projetos_autor_periodo2)) + '% no período')
    print('Saúde: ' + str(qtd_saude2) + ' - ' + str(get_percentual_categoria(qtd_saude2, total_projetos_autor_periodo2)) + '% no período')
    print('Infra: ' + str(qtd_infra2) + ' - ' + str(get_percentual_categoria(qtd_infra2, total_projetos_autor_periodo2)) + '% no período')
    print('Economia: ' + str(qtd_economia2) + ' - ' + str(get_percentual_categoria(qtd_economia2, total_projetos_autor_periodo2)) + '% no período')
    print('Outros: ' + str(qtd_outros2) + ' - ' + str(get_percentual_categoria(qtd_outros2, total_projetos_autor_periodo2)) + '% no período')

    output.gerar_grafico_estrela2(autor2, qtd_educacao2, qtd_seguranca2, qtd_saude2, qtd_infra2, qtd_economia2, qtd_outros2)

##################################### Captura quantidade páginas definidas pelo usuário #####################################
