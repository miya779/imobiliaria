from bs4 import BeautifulSoup
import requests, re, time
import pandas as pd
from selenium import webdriver
from urllib.parse import urljoin


#selenium Firefox driver
driver = webdriver.Firefox()

# O link deve estar ordenado por preço ascendente para garantir que o script irá funcionar
url1 = "https://www.vivareal.com.br/venda/sp/atibaia/bairros/caetetuba/apartamento_residencial/?pagina="
url2 = "#onde=Brasil,S%C3%A3o%20Paulo,Atibaia,Bairros,Caetetuba,,,,BR%3ESao%20Paulo%3ENULL%3EAtibaia%3EBarrios%3ECaetetuba,,,&ordenar-por=preco:ASC" # site


current_page = 1
last_page = 1

df = pd.DataFrame(columns=['valor_m2','valor','m2','quartos','vagas','endereco','link'])

while current_page <= last_page:
    print("\nPage: " + str(current_page))
    url_pagination = url1 + str(current_page) + url2
    driver.get(url_pagination)
    time.sleep(4)
    response = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.find_all('a',class_="property-card__content-link")
    #pagination
    ul_pages = soup.find_all('ul',class_="pagination__wrapper")[0]
    li_pages = ul_pages.find_all('li')
    last_page = int(li_pages[-2].text)
    #end pagination
    for link in links:
        endereco = link.find("span",{"class":"property-card__address"}).text
        info = link.find_all("span",{"class":"property-card__detail-value"})
        m2 = float(re.findall(r'\d+',info[0].text)[0])
        quartos = int(re.findall(r'\d+',info[1].text)[0]) if re.findall(r'\d+',info[1].text) else 0
        banheiros = int(re.findall(r'\d+',info[2].text)[0]) if re.findall(r'\d+',info[2].text) else 0
        vagas = int(re.findall(r'\d+',info[3].text)[0]) if re.findall(r'\d+',info[3].text) else 0
        valor = link.find_all("div",{"class":"property-card__price"})[0].find('p').text if link.find_all("div",{"class":"property-card__price"})[0].find('p') else 0
        if valor != 0:
            valor = float(''.join(re.findall(r'\d+',valor)))
        valor_condominio = link.find_all("strong",{"class":"js-condo-price"})
        if valor_condominio:
            valor_condominio = float(valor_condominio[0].text.replace('R$ ','').replace('.',''))
        else:
            valor_condominio = 0.0
        valor_m2 = valor/m2
        link_href = link['href']
        link_href = urljoin(url_pagination, link_href)
        df.loc[len(df)] = [valor_m2, valor, m2, quartos, vagas, endereco, link_href]
    current_page +=1


driver.close()

df = df.sort_values(by="valor_m2")
df.to_csv('viva_real.csv', index=False)    

