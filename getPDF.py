"""
Apos listar todos os CVM em tabela, pegar, de cada empresa/CVM, a DFP mais recente com status de 'Ativo'
Clicar em 'Visualizar o Documento' e navegar pela nova página
Clicar no <select> 'DFs Consolidadas' e selecionar 'Pareceres e Declarações'
Clicar em 'Salvar em PDF' e navegar pelo popup
Desmarcar 'Todos' e marcar 'Relatório o Auditor Independente'
Clicar em 'Gerar PDF'

Renomear PDF e salvar em diretorios:
    formato 'PPAs/PPA-2021-Empresa/*.pdf'
"""



''' libs imports '''
import os # operational system and filesystem manipulation
import time # timeset library
from datetime import datetime # datetime consult library
import pandas as pd # to databases and data manipulation functions
from selenium import webdriver # do autotests on browser
# simulate clicks and typing
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select # verify if tag is a 'select'
from selenium.webdriver.support.ui import WebDriverWait # makes webdrive wait page load
from selenium.webdriver.support import expected_conditions as EC # verify if expected conditions is valid
from selenium.webdriver.chrome.options import Options # chrome webdriver options
from webdriver_manager.chrome import ChromeDriverManager # chrome webdriver manager


''' webdriver config '''
option = Options()
option.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option) # call the webdriver - installed on cache - to open the browser and get the URL


''' data and targets '''
df_docsHref = pd.read_excel('./data/documentos.xlsx')
targets = {
	# button
	'generatePDF': {'id': "btnGeraRelatorioPDF"},
	'savePDF': {'id': "btnConsulta"},
	# a/checkbox
	'checkAll': {
		'id': "0_anchor",
		'className': "jstree-anchor  jstree-clicked",
		'text': "Todos"
	},
	'checkReport': {
		'id': "1655_anchor",
		'className': "jstree-anchor",
		'text': "Relatório do Auditor Independente  - Sem Ressalva"
	},
	# popup
	'genPDFModal': {'id': "iFrameModal"}
}


''' PDF local storage '''
def documentStorage(doc):
	output = f"./PPAs/PPA-{doc['data'].replace('/', '_').split(' ')[0]}-{doc['nomeEmpresa'].replace(' ', '_')}"
	os.mkdir(output)
	files = os.listdir()
	for file in files:
		if file.split('.')[-1] == 'pdf':
			os.replace(file, f"{output}/{doc['codigo']}.pdf")


''' PDF download routine '''
def documentDownload(docsURL):
	for i, doc in docsURL.iterrows():
		# limiter
		if i > 5:
			break
		URL = "https://www.rad.cvm.gov.br/ENET/" + doc['linkDownload']
		driver.get(URL)
		time.sleep(6.8)
		driver.find_element_by_id(targets['generatePDF']['id']).click()
		time.sleep(5)
		driver.switch_to.frame(targets['genPDFModal']['id'])
		time.sleep(0.7)
		driver.find_element_by_xpath(f"\
			//a[@id='{targets['checkAll']['id']}']\
			[contains(text(), '{targets['checkAll']['text']}')]\
			[@class='{targets['checkAll']['className']}']"
		).click()
		time.sleep(0.6)
		driver.find_element_by_xpath(f"\
			//a[@id='{targets['checkReport']['id']}']\
			[@class='{targets['checkReport']['className']}']"
		).click()
		time.sleep(0.6)
		driver.find_element_by_id(targets['savePDF']['id']).click()
		time.sleep(17)
		documentStorage(doc)


''' run '''
try:
	os.mkdir("./PPAs")
except:
	None
documentDownload(df_docsHref)

