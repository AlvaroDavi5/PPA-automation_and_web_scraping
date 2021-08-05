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


options = Options()
options.headless = True
PATH = 'webdriver/chromedriver.exe'
url = 'https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx'

driver = webdriver.Chrome(ChromeDriverManager().install()) # call the webdriver - installed on cache - to open the browser and get the URL
#driver = webdriver.Chrome()
#driver = webdriver.Chrome(PATH, options=options) # call the webdriver - using bin/exe file - to open the browser and get the URL

codEmpresaId = 'cboEmpresa'
dataInicioId = 'txtDataIni'
dataFimId = 'txtDataFim'
categoriaId = 'cboCategorias'
radioPeriodoId = 'rdPeriodo'
retornoAutoComplete = 'retornoAutoComplete'
botaoSubmit = 'btnConsulta'
resultTable = 'grdDocumentos'
dataAtual = datetime.today().strftime('%d/%m/%Y')
documentsDict = {'codigo':[],
                 'nomeEmpresa':[],
                 'data':[],
                 'status':[],
                 'linkDownload':[]}
codigos = []
erros = {'empresa':[],
         'codigo':[]}

driver.get(url)
time.sleep(5)

#Pega codigos das empresas
def getCompanyCodes():
    codigosDF = pd.read_excel('codigos.xlsx', converters={'codigo':str})
    for index, row in codigosDF.iterrows():
        codigos.append(row)

#Pega dados da tabela gerada e salva no dict
def getTableData():
    linhas = driver.find_elements_by_xpath('//*[@id="grdDocumentos"]/tbody/tr')
    for linha in linhas:
        documentsDict['codigo'].append(linha.find_elements_by_tag_name('td')[0].get_attribute('innerText'))
        documentsDict['nomeEmpresa'].append(linha.find_elements_by_tag_name('td')[1].get_attribute('innerText'))
        documentsDict['data'].append(linha.find_elements_by_tag_name('td')[6].get_attribute('innerText'))
        documentsDict['status'].append(linha.find_elements_by_tag_name('td')[7].get_attribute('innerText'))
        colunaDownload = linha.find_elements_by_tag_name('td')[10]
        link = colunaDownload.find_elements_by_tag_name('i')[0].get_attribute('onclick')
        documentsDict['linkDownload'].append(link[14:96])

#Adiciona uma empresa à pesquisa pelo código
def addCompanyToSearch(row):
    codEmpresa = driver.find_element_by_id(codEmpresaId)
    codEmpresa.send_keys(row['codigo'])
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-menu-item')))
    WebDriverWait(driver, 15).until(EC.invisibility_of_element((By.ID, 'divSplash')))
    opcao = driver.find_element_by_class_name('ui-menu-item')
    opcoes = driver.find_elements_by_class_name('ui-menu-item')
    if(len(opcoes)>1):
        print(row['codigo'])
        erros['codigo'].append(row['codigo'])
        erros['empresa'].append(row['empresa'])
    opcao.click()

#Adiciona todas empresas da base a pesquisa
def addCompaniesToSearch():
    getCompanyCodes()
    for row in codigos:
        addCompanyToSearch(row)

#Escolhe opção de período
def radioPeriod():
    radioData = driver.find_element_by_id(radioPeriodoId)
    radioData.click()

#Coloca data inicial
def iniDate():
    inputDataIni = driver.find_element_by_id(dataInicioId)
    inputDataIni.send_keys('31/12/2016')
    inputDataIni.send_keys(Keys.ENTER)

#Coloca data final
def endDate():
    inputDataFim = driver.find_element_by_id(dataFimId)
    inputDataFim.send_keys(dataAtual)
    inputDataFim.send_keys(Keys.ENTER)

#Coloca categoria
def chooseCategory():
    categorias = driver.find_element_by_xpath('//*[@id="cboCategorias_chosen"]')
    categorias.click()
    inputCategoria = driver.find_element_by_xpath('//*[@id="cboCategorias_chosen"]/div/ul/li[22]')
    inputCategoria.click()

#Faz submit no form para gerar tabela
def submitForm():
    driver.find_element_by_id(botaoSubmit).click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, botaoSubmit)))

addCompaniesToSearch()
df2 = pd.DataFrame(erros) 
df2.to_excel("erros.xlsx")  
print('CABO')
'''
#getTableData()
#print(documentsDict)
'''


