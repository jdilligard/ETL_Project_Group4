#!/usr/bin/env python
# coding: utf-8


#Import the important libraries
from time import time,sleep
from random import randint
from IPython.core.display import clear_output
from requests import get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re 


def CarFaxVehicleScrapper(url):
    #scraping webpage with beautiful soup
    response = get(url, timeout = 5)
    soup = BeautifulSoup(response.text, 'html.parser')

    mm = soup.select('.disclaimer-vehicle-title')
    mm = str(mm[0].contents[0]).strip().split()
    data = soup.select('.vehicle-info-details')



    if(len(mm) < 4):
        mm.append('-')
        mm.append('-')

    try:
        info = []
        for d in data:
            info.append(str(d.contents[0]).strip())



        vehicle_info = {
            "vin": info[23],
            'year': mm[0],
            'make': mm[1],
            'model': mm[2],
            'trim' : mm[3],
            "price": info[1],
            "mileage": info[3],
            "location": info[5],
            "ext_color": info[7],
            "int_color": info[9],
            "drive_type": info[11],
            "transmission": info[13],
            "body_style": info[15],
            "engine": info[17],
            "fuel": info[19],
            "mpg": info[21],
            "stock_num": info[25]    
        }

    except:
        print('found a weird car. putting in blanks for that one...')
        vehicle_info = {
            "vin": '',
            'year': '',
            'make': '',
            'model': '',
            'trim' : '',
            "price": '',
            "mileage": '',
            "location": '',
            "ext_color": '',
            "int_color": '',
            "drive_type": '',
            "transmission": '',
            "body_style": '',
            "engine": '',
            "fuel": '',
            "mpg": '',
            "stock_num": ''   
        }

    
    #parsing out the dealer info
    temp = soup.select('.dealer-name')
    dealer_name = str(temp[0].contents[0]).strip()
    dealer_name    


       #parsing out the dealer address - NOTICE I USED # for an id
    temp = soup.select('#dealer-info__address-text')
    dealer_street = str(temp[0].contents[0]).strip()
    try:
        dealer_csz = str(temp[0].contents[2]).strip()
        string3 = dealer_csz
        strg = string3.strip().split(',')
        len(strg)
        city = strg[0]
        strg = strg[1].split()
        state = strg[0]
        zipc = strg[1]
    except:
        print('something went wrong with the address')
        city = '-'
        state = '-'
        zipc = '-'


    temp = soup.select('.dealer-info__phone-text')
    dealer_phone = str(temp[0].contents[0]).strip()


    dealer_info = {
        #'vin' : info[23],
        'dealer_name': dealer_name,
        'dealer_street': dealer_street,
        'dealer_city': city,
        'dealer_state': state,
        'dealer_zip': zipc,
        'dealer_phone': dealer_phone,
       # 'stock_number': info[25]
    }


    
    try:
        dealer_info['vin'] = info[23]
        dealer_info['stock_number'] = info[25]
    except:
        dealer_info['vin'] = ''
        dealer_info['stock_number'] = ''
            
    vehicle_info['dealer_info'] = dealer_info
    vehicle_info
       
    
    return vehicle_info


def scrapper_to_pandas(url):
    print('in the scrapper_to_pandas')
    executable_path = {'executable_path': r"C:\Users\jdilligard\Desktop\chromedriver_win32\chromedriver.exe"}
    #browser = Browser('chrome', **executable_path, headless=False)

    #url = 'https://www.carfax.com/Used-Jeep-Cherokee-Dallas-TX_w371_c18864'
    #browser.visit(url)


    try:
    #scraping webpage with beautiful soup
        response = get(url, timeout = 5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print('There is a fly in my beautifulsoup. I can not read this page. Make sure that there are cars that meet your requirements.')
        return

    data = soup.find(id='listing_0').find('a')['href']
    #print(data)

    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("/vehicle/")}):
        #print(link.get('href'))
        string = 'https://www.carfax.com' + link.get('href')
        links.append(string)
        #print(string)

    links = list(set(links))

    clean_links = []
    data2 = []
    for link in links:
        link = link.replace('.com//','.com/')
        if(link not in clean_links):
            clean_links.append(link)
            print(link)
            data2.append(CarFaxVehicleScrapper(link))


    all_dealers = [x['dealer_info'] for x in data2]

    dealer_df = pd.DataFrame(all_dealers)
    dealer_df.head()


    vin= [k['vin'] for k in data2]
    make=[k['make'] for k in data2]
    model=[k['model'] for k in data2]
    ext_color= [k['ext_color'] for k in data2]
    int_color= [k['int_color'] for k in data2]
    body_style= [k['body_style'] for k in data2]
    year= [k['year'] for k in data2]


    list_of_descriptions= list(zip(vin,make,model,ext_color,int_color,body_style,year))

    car_descriptions_df=  pd.DataFrame(list_of_descriptions, columns=['vin','make','model','ext_color','int_color','body_style','year'])

    car_descriptions_df.head()

    mileage= [k['mileage'] for k in data2]
    location= [k['location'] for k in data2]

    v_info_list = list(zip(vin,mileage,location))

    v_info_df= pd.DataFrame(v_info_list, columns=['vin','mileage','location'])

    v_info_df.head()

    drive_type= [k['drive_type'] for k in data2]
    engine= [k['engine'] for k in data2]
    transmission= [k['transmission'] for k in data2]
    mpg= [k['mpg'] for k in data2]
    fuel= [k['fuel'] for k in data2]

    drive_train_list= list(zip(vin,drive_type,engine,transmission,mpg,fuel))

    drive_train_df= pd.DataFrame(drive_train_list, columns= ['vin','drive_type','engine', 'transmission', 'mpg', 'fuel'])

    drive_train_df.head()

    price= [x['price'] for x in data2]
    price_list= list(zip(vin,price))
    price_df= pd.DataFrame(price_list, columns=['vin', 'price'])
    price_df.head()

    
    
    dict = {
        'dealer' : dealer_df,
        'car_descriptions': car_descriptions_df,
        'vehicle_info': v_info_df,
        'drive_train': drive_train_df,
         'price': price_df 
    }
    print('Done with scrapper_to_pandas')
    return dict
