import nltk
from nltk.corpus import wordnet
import output

# nltk.download('wordnet')
#nltk.download('omw')

st = nltk.stem.RSLPStemmer()
stopwords = set(nltk.corpus.stopwords.words('portuguese'))
_processar_categorias = True;
caminho_raiz = 'D:/TCC2/palavra_categorias/';

def unique(lista):
    return list(set(lista))

def configurar(processar_categorias = True):
    _processar_categorias = processar_categorias

def remove_stopwords(expressao):
    palavras = [i for i in expressao.split() if not i in stopwords]
    return (" ".join(palavras))

def gerar_palavras_educacao():
    caminho_arquivo_palavras = caminho_raiz + 'educacao.txt'

    if (not _processar_categorias):
        return output.carregar_palvaras_categoria_arquivo(caminho_arquivo_palavras);

    palavras_diretas = [st.stem('escola'), st.stem('laboratório'), st.stem('educação'), st.stem('informática')]
    educacao_palavras = []

    for palavra_direta in palavras_diretas:
        educacao_palavras.append(palavra_direta)
        for synsets in wordnet.synsets(palavra_direta, lang='por'):
            for i in synsets.lemma_names(lang='por'):
                educacao_palavras.append(st.stem(i))

    palavras_unificadas = unique(educacao_palavras);
    output.salvar_palavras_categoria_arquivo(palavras_unificadas, caminho_arquivo_palavras)
    return palavras_unificadas;

def gerar_palavras_seguranca():
    caminho_arquivo_palavras = caminho_raiz + 'seguranca.txt'

    if (not _processar_categorias):
        return output.carregar_palvaras_categoria_arquivo(caminho_arquivo_palavras);

    palavras_diretas = [st.stem('policial'), st.stem('assalto'), st.stem('roubo')]

    seguranca_palavras = []
    for palavra_direta in palavras_diretas:
        seguranca_palavras.append(palavra_direta)
        for synsets in wordnet.synsets(palavra_direta, lang='por'):
            for i in synsets.lemma_names(lang='por'):
                seguranca_palavras.append(st.stem(i))

    palavras_unificadas = unique(seguranca_palavras);
    output.salvar_palavras_categoria_arquivo(palavras_unificadas, caminho_arquivo_palavras)
    return palavras_unificadas;

def gerar_palavras_saude():
    caminho_arquivo_palavras = caminho_raiz + 'saude.txt'

    if (not _processar_categorias):
        return output.carregar_palvaras_categoria_arquivo(caminho_arquivo_palavras);

    palavras_diretas = [st.stem('vacinação')]
    saude_palavras = []

    for palavra_direta in palavras_diretas:
        saude_palavras.append(palavra_direta)
        for synsets in wordnet.synsets(palavra_direta, lang='por'):
            for i in synsets.lemma_names(lang='por'):
                saude_palavras.append(st.stem(i))

    palavras_unificadas = unique(saude_palavras);
    output.salvar_palavras_categoria_arquivo(palavras_unificadas, caminho_arquivo_palavras)
    return palavras_unificadas;

def gerar_palavras_infra():
    caminho_arquivo_palavras = caminho_raiz + 'infra.txt'

    if (not _processar_categorias):
        return output.carregar_palvaras_categoria_arquivo(caminho_arquivo_palavras);

    palavras_diretas = [st.stem('prolongamento'), st.stem('via'), st.stem('praça')]
    infra_palavras = []

    for palavra_direta in palavras_diretas:
        infra_palavras.append(palavra_direta)
        for synsets in wordnet.synsets(palavra_direta, lang='por'):
            for i in synsets.lemma_names(lang='por'):
                infra_palavras.append(st.stem(i))

    palavras_unificadas = unique(infra_palavras);
    output.salvar_palavras_categoria_arquivo(palavras_unificadas, caminho_arquivo_palavras)
    return palavras_unificadas;

def gerar_palavras_economia():
    caminho_arquivo_palavras = caminho_raiz + 'economia.txt'

    if (not _processar_categorias):
        return output.carregar_palvaras_categoria_arquivo(caminho_arquivo_palavras);

    palavras_diretas = [st.stem('orçamento'), st.stem('financeiro'), st.stem('fundos'), st.stem('créditos'), st.stem('pagamentos'), st.stem('auxílio')]
    economia_palavras = []

    for palavra_direta in palavras_diretas:
        economia_palavras.append(palavra_direta)
        for synsets in wordnet.synsets(palavra_direta, lang='por'):
            for i in synsets.lemma_names(lang='por'):
                economia_palavras.append(st.stem(i))

    palavras_unificadas = unique(economia_palavras);
    output.salvar_palavras_categoria_arquivo(palavras_unificadas, caminho_arquivo_palavras)
    return palavras_unificadas;

def processa_categoria(titulo_projeto, educacao_palavras, seguranca_palavras, saude_palavras, infra_palavras, economia_palavras):
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
    if (len(categorias_projetos) == 0):
        categorias_projetos.append('Outros')

    return categorias_projetos