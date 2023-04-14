from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urljoin

url = "https://loft.com.br/venda/imoveis/sp/sao-paulo/jardim-paulista_sao-paulo_sp?pagina=" # site

url_pagination = url + "1"
response = requests.get(url_pagination) 

df = pd.DataFrame(columns=['valor_m2','valor','m2','quartos','vagas','tipo','endereco','link'])

soup = BeautifulSoup(response.content, 'html.parser')

#pagination
ul_pages = soup.find_all('ul',class_="MuiPagination-ul")[0]
a_pages = ul_pages.find_all('a')
total_pages = int(a_pages[len(a_pages)-1].text)
#end pagination

for i in range(1, total_pages+1):
    print("\nPage: " + str(i))
    if i != 1:
        url_pagination = url + str(i)
        response = requests.get(url_pagination) 
        soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a',class_="jss260")
    for link in links:
        tipo = link.find("span",{"class":"jss274"}).text
        endereco = link.h2.text
        info = link.findAll("span",{"class":"jss126"})
        m2 = int(info[0].text.replace('m²',''))
        quartos = int(info[1].text)
        vagas = int(info[2].text)
        valor = int(link.find("span",{"class":"jss148"}).text.replace('R$ ','').replace('.',''))
        valor_m2 = valor/m2
        link_href = link['href']
        link_href = urljoin(url, link_href)
        df.loc[len(df)] = [valor_m2, valor, m2, quartos, vagas, tipo, endereco, link_href]
        #single_page = requests.get(link_href)
        #singleSoup = BeautifulSoup(single_page.content, 'html.parser')
        #iptu = 
        #valor_condominio = 
        #nome_condominio = 
        #banheiros = 


df = df.sort_values(by="valor_m2")
df.to_csv('imoveis.csv', index=False)    

