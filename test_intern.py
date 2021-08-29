#!/usr/bin/python3
import requests, re, json, time
from fake_useragent import UserAgent
import novocib_def
from bs4 import BeautifulSoup
import sqlite3


# con = sqlite3.connect(":memory:")

try:
	with open('/home/mikhail/python_cod/kvartiri_link.txt', 'r') as f:
	    kvartiri_links = f.read().split('\n')
except:
	first_page_link = []
	doms_links = []
	kvartiri_links = []
	count_doms = 10
	pause = 1
	start_link = 'https://novosibirsk.n1.ru'

	def get_soup(url):
		r = requests.get(url, headers={'User-Agent': UserAgent().ie})
		soup = BeautifulSoup(r.content, 'html.parser')
		return soup

	url = 'https://novosibirsk.n1.ru/kupit/kvartiry/vtorichka/?floor_min=9'
	soup = get_soup(url)

	a_list = soup.find_all('a', attrs={'class':'link'})

	for row in a_list:
		if '/view/' in row['href']:
			first_page_link.append(start_link + row['href'])

	print(first_page_link)
	a_list = []
	print('Цикл по поиску домов')
	for i_link in first_page_link:
	    print(i_link)
	    soup = get_soup(i_link)
	    try:
		    a_tag = soup.find('a', attrs={'class':'card-living-content-params__more-offers'})
		    print(a_tag)
		    dom_link = start_link + a_tag['href']
		    if dom_link not in doms_links and len(doms_links) < count_doms:
		        soup = get_soup(dom_link)
		        a_list = soup.find_all('a', attrs={'class':'link'})
		        print('Цикл по поиску квартир')
		        for row in a_list:
		        	if '/view/' in row['href']:
		        		kvartiri_links.append(start_link + row['href'])
		        	time.sleep(pause)
		        	#print('Ищем следующую квартиру')
		        doms_links.append(dom_link)
	    except:
	        pass
	    print('Ищем следующий дом')
	    print(str(len(doms_links)))

	with open('/home/mikhail/python_cod/kvartiri_link.txt', 'w') as f:
	    f.write('\n'.join(kvartiri_links))

# 0id_kvartiri, 1adress, 2square, 3floor, 4year, 5price, 6material, 7location, 8date

con = sqlite3.connect('/home/mikhail/python_cod/novocib_DB.db') # Соединение с Базой данных
cur = con.cursor() 
cur.execute("create table IF NOT EXISTS KVARTIRA (id_kvartiri, adress, square, floor, year, material, location, CONSTRAINT new_pk_kv PRIMARY KEY (id_kvartiri))")
cur.execute("create table IF NOT EXISTS PRICE (id_kvartiri, price, date, CONSTRAINT new_pk_pr PRIMARY KEY (id_kvartiri, date))")

data_kvartira = []
for link in kvartiri_links:
	
	try:
		data_kvartira.append(novocib_def.get_data(link))
		
	except:
		pass
for row in data_kvartira:
	try:
		cur.execute("insert into KVARTIRA values (?, ?, ?, ?, ?, ?, ?)", (row[0],row[1],row[2],row[3],row[4],
							row[6],row[7]))
	except:
		#print('Проблемы с записью в таблицу Квартиры')
		pass
	try:
		cur.execute("insert into PRICE values (?, ?, ?)", (row[0],row[5],row[8]))
	except:
		#print('Проблемы с записью в таблицу Цены')
		pass
con.commit() # Сохранение изменений в Базе данных
con.close() # Закрытие соединения с Базой данных