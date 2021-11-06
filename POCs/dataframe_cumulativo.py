import pandas as pd

data1 = [
    ['Projeto1', 'Autor1', '31/12/2011', 'Categoria1'],
    ['Projeto2', 'Autor2', '31/12/2012', 'Categoria2']
];

data2 = [
    ['Projeto2', 'Autor2', '31/12/2012', 'Categoria2']
];

df = pd.DataFrame(data1, columns = ['Projetos', 'Autores', 'Data', 'Categorias'])

caminho = 'D:/Temp/df.csv'
# df.to_csv(caminho);
# df_lido = pd.read_csv(caminho)
# df_lido = df_lido.append(data2)

print(df)
print('')
print(df['Projetos'][0])
# print(df[1])

#print(df_lido)

