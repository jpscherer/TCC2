import nltk
import sys
from nltk.corpus import wordnet
sys.path.insert(0, 'D:/Projects/TCC2/Camara_Vereadores_bnu')

from categoria_helper import gerar_palavras_educacao, gerar_palavras_seguranca, gerar_palavras_saude, gerar_palavras_infra, gerar_palavras_economia

print(gerar_palavras_infra())

# nltk.download('wordnet')
# nltk.download('omw')

# st = nltk.stem.RSLPStemmer()
#
# for synsets in wordnet.synsets('escola', lang='por'):
#     print(synsets.lemma_names(lang='por'))
    # for lemma in synsets.lemmas():
    #     print(lemma.name())




# import pandas as pd
# data1 =  { 'Projetos' : ['abc','cba'],
#               'Autores': ['a1', 'a2'],
#               'Categorias': ['c1', 'c2']
#             }
# data2 =  { 'Projetos' : ['xxx','zzz'],
#               'Autores': ['a3', 'a4'],
#               'Categorias': ['c3', 'c4']
#             }
#
# df = pd.DataFrame(data1, columns = ['Projetos', 'Autores', 'Categorias']);
# df2 = pd.DataFrame(data2, columns = ['Projetos', 'Autores', 'Categorias'])
#
# df.append(df2, ignore_index=True)
#
# print(df);


# Importing pandas as pd
# import pandas as pd
#
# # Creating the first Dataframe using dictionary
# df1 = df = pd.DataFrame({"a": [1, 2, 3, 4],
#                          "b": [5, 6, 7, 8]})
#
# # Creating the Second Dataframe using dictionary
# df2 = pd.DataFrame({"a": [1, 2, 3],
#                     "b": [5, 6, 7]})
#
# # Print df2
# df1 = df1.append(df2, ignore_index = True)
#
# # Print df1
# print(df1, "\n")