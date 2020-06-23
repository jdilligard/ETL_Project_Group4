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
        
    #parsing out the dealer info
    temp = soup.select('.dealer-name')
    dealer_name = str(temp[0].contents[0]).strip()
    dealer_name    

    #parsing out the dealer address - NOTICE I USED # for an id
    temp = soup.select('#dealer-info__address-text')
    dealer_street = str(temp[0].contents[0]).strip()
    dealer_csz = str(temp[0].contents[2]).strip().split()



    temp = soup.select('.dealer-info__phone-text')
    dealer_phone = str(temp[0].contents[0]).strip()


    dealer_info = {
        'vin' : info[23],
        'dealer_name': dealer_name,
        'dealer_street': dealer_street,
        'dealer_city': dealer_csz[0],
        'dealer_state': dealer_csz[1],
        'dealer_zip': dealer_csz[2],
        'dealer_phone': dealer_phone,
        'stock_number': info[25]
    }

    vehicle_info['dealer_info'] = dealer_info
    vehicle_info

    return vehicle_info



