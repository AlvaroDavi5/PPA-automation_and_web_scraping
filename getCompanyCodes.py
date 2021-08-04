import pandas as pd

sheet = pd.read_excel('base.xlsx', sheet_name=['Base a ser Feita'], converters={'ID da\nempresa':str})
df = sheet['Base a ser Feita']
codigosSeries = df['ID da\nempresa']
codigosSeries = codigosSeries.drop_duplicates()
codigos = []

for index, value in codigosSeries.items():
    codigos.append(str(value))

for codigo in codigos:
    if len(codigo) < 5:
        codigos.remove(codigo)

df2 = pd.DataFrame(codigos)  
df2.to_excel("codigos.xlsx")  

