import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
                 'linkDownload':[]}
codigos = []
erros = {'empresa':[],
         'codigo':[]}

driver.get(url)
time.sleep(5)

#Pega codigos das empresas
def getCompanyCodes():
    codigosDF = pd.read_excel('./data/codigos.xlsx', converters={'codigo':str})
    for index, row in codigosDF.iterrows():
        codigos.append(row)

#Pega dados de uma página da tabela gerada e salva no dict
def getTablePageData():
    linhas = driver.find_elements_by_xpath('//*[@id="grdDocumentos"]/tbody/tr')
    for linha in linhas:
        status = linha.find_elements_by_tag_name('td')[7].get_attribute('innerText')
        if status == 'Ativo':
            documentsDict['codigo'].append(linha.find_elements_by_tag_name('td')[0].get_attribute('innerText'))
            documentsDict['nomeEmpresa'].append(linha.find_elements_by_tag_name('td')[1].get_attribute('innerText'))
            documentsDict['data'].append(linha.find_elements_by_tag_name('td')[6].get_attribute('innerText'))
            colunaDownload = linha.find_elements_by_tag_name('td')[10]
            link = colunaDownload.find_elements_by_tag_name('i')[0].get_attribute('onclick')
            documentsDict['linkDownload'].append(link[14:96])

#Pega dados da tabela gerada e salva no dict
def getTableData():
    nextBtn = driver.find_element_by_id('grdDocumentos_next')
    while(nextBtn.get_attribute('class') == 'paginate_button next'):
        getTablePageData()
        nextBtn.click()
        nextBtn = driver.find_element_by_id('grdDocumentos_next')
        if nextBtn.get_attribute('class') != 'paginate_button next':
            getTablePageData()
            break  

#Adiciona uma empresa à pesquisa pelo código
def addCompanyToSearch(row):
    codEmpresa = driver.find_element_by_id(codEmpresaId)
    codEmpresa.send_keys(row['codigo'])
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ui-menu-item')))
    WebDriverWait(driver, 15).until(EC.invisibility_of_element((By.ID, 'divSplash')))
    opcao = driver.find_element_by_class_name('ui-menu-item')
    opcao.click()

#Adiciona todas empresas da base a pesquisa
def addCompaniesToSearch():
    getCompanyCodes()
    for row in codigos:
        addCompanyToSearch(row)

#Escolhe opção de período
def radioPeriod():
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, radioPeriodoId))).click()

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
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'cboCategorias_chosen'))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cboCategorias_chosen"]/div/ul/li[22]'))).click()

#Faz submit no form para gerar tabela
def submitForm():
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, botaoSubmit))).click()
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.ID, botaoSubmit)))

radioPeriod()
iniDate()
endDate()
chooseCategory()
addCompaniesToSearch()
submitForm()
getTableData()
documentsDF = pd.DataFrame(documentsDict)
documentsDF.to_excel("./data/documentos.xlsx") 



