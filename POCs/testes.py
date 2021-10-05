# import nltk
# from nltk.corpus import wordnet
# #nltk.download('wordnet')
#
# st = nltk.stem.RSLPStemmer()
#
# for synsets in wordnet.synsets():
#     print(synsets.lemma_names())
#     # for lemma in synsets.lemmas():
#     #     print(lemma.name())




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
import pandas as pd

# Creating the first Dataframe using dictionary
df1 = df = pd.DataFrame({"a": [1, 2, 3, 4],
                         "b": [5, 6, 7, 8]})

# Creating the Second Dataframe using dictionary
df2 = pd.DataFrame({"a": [1, 2, 3],
                    "b": [5, 6, 7]})

# Print df2
df1 = df1.append(df2, ignore_index = True)

# Print df1
print(df1, "\n")