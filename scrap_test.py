# -*- coding: utf-8 -*-
#import the library used to query a website
import certifi
import urllib3
import socks
import socket
import time
import os
from stem import Signal
from stem.control import Controller
import requests
from bs4 import BeautifulSoup
import PIL
from resizeimage import resizeimage
from PIL import Image
from pytesseract import *

def ocr(company_email_src):
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR"'
    pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    img_url = bou+company_email_src
    connection_pool = urllib3.PoolManager()
    http = urllib3.PoolManager()
    r = http.request('GET', img_url, preload_content=False)

    with open('a.tif', 'wb') as out:
        while True:
            data = r.read(1)
            if not data:
                break
            out.write(data)

    r.release_conn()

    img = Image.open('C:\\Users\\----\\a.tif')
    baseheight = 34
    wpercent = (baseheight/float(img.size[1]))
    wsize = int((float(img.size[0])*float(wpercent)))
    img = img.resize((wsize,baseheight), PIL.Image.ANTIALIAS)
    company_email = pytesseract.image_to_string(img)
    return company_email 

def scrap_info(address):
    page_body = requests.get(address, allow_redirects=False).text               #pobiera stronę
    soup = BeautifulSoup(page_body,'html.parser')                               #supuje

    company_name=soup.find('h1',{"itemprop" : 'name'}).get_text()               
    street=soup.find('span',{"itemprop" : 'streetAddress'}).get_text()
    postal=soup.find('span',{"itemprop" : 'postalCode'}).get_text()
    city=soup.find('span',{"itemprop" : 'addressLocality'}).get_text()
    company_add = street + " " + postal  + " " + city
    company_woj=soup.find('div',{"class" : 'txtDataBox marginTop10'}).get_text()
    company_tel=soup.find('section',{"id" : 'telBox'}).get_text()
    company_bra=soup.find('ul',{"id" : 'brLst'}).get_text()
    try:
        company_www=soup.find('a',{"class" : 'wizLnk allCornerRound3'}).get('href')
    except:
        company_www = 'brak'
    try:
        company_email_src = soup.find('img',{"alt" : 'główny adres kontaktowy e-mail do firmy'}).get("src")
    except:
        company_email_src = 'brak'
    print(company_name)
#    print(company_add)
#    print(company_woj)
#    print(company_tel)
#    print(company_bra)
#    print(company_www)
#    print(company_email_src)

    if company_email_src != 'brak':
        company_email = ocr(company_email_src)
        text_file = open("Output2.txt", "a")
        text_file.write(company_name+"\t"+ company_add+"\t"+ company_woj+"\t"+ company_tel+"\t"+ company_bra +"\t"+ company_www+"\t"+ company_email +"\n")
        text_file.close()
        print('zapisano')  
        return 0


    text_file = open("Output2.txt", "a")
    text_file.write(company_name+"\t"+ company_add+"\t"+ company_woj+"\t"+ company_tel+"\t"+ company_bra +"\t"+ company_www+"\t"+"\n")
    text_file.close()
    print('zapisano')  
    return 0

with Controller.from_port(port = 9151) as controller:
    controller.authenticate()
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9150)
    socket.socket=socks.socksocket

    list_dir="C:\\-------\\src\\"
    url1 = "-----------"
    url2 = "---------------"
    bou = "--------------"    #beginning of url
    list_of_pages = []

    nr_of_all_pages = list(range(3,5))
    #page = requests.Session()
    for nr_of_page in nr_of_all_pages:
        print('Przejscie do strony ' + str(nr_of_page) +' z '+str(nr_of_all_pages)) ograniczenie do przegladania tylko kilku stron
        
        page_body = requests.get(url1 + str(nr_of_page) + url2, allow_redirects=False).text
        soup = BeautifulSoup(page_body,'html.parser')
        #right_table=soup.find('table',{"class" : 'przeppoz'})

        all_links=soup.find_all('a', class_='wizLnk')
        for link in all_links :
            list_of_pages.insert(0,link.get("href"))
            scrap_info(list_of_pages[0])

    
    controller.signal(Signal.NEWNYM)
    time.sleep(controller.get_newnym_wait())      
