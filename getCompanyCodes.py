import pandas as pd

sheet = pd.read_excel('base.xlsx', sheet_name=['Base a ser Feita'], converters={'ID da\nempresa':str})
df = sheet['Base a ser Feita']
codigosSeries = df[['Nome','ID da\nempresa']]
codigosSeries = codigosSeries.drop_duplicates()
codigosSeries.columns = ['empresa', 'codigo']
codigosSeries.to_excel("codigos.xlsx")  

