from time import time,sleep
from random import randint
#from IPython.core.display import clear_output
from requests import get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re 
import pymongo
from splinter import Browser

import Scrapper


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"C:\Program Files\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    
    
def scrape_info():    
    url = 'https://www.carfax.com/Used-Jeep-Cherokee-Dallas-TX_w371_c18864'
    
    #scraping webpage with beautiful soup
    response = get(url, timeout = 5)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #data = soup.find(id='listing_0').find('a')['href']
    
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("/vehicle/")}):
    #print(link.get('href'))
        string = 'https://www.carfax.com' + link.get('href')
        links.append(string)
    
    links = list(set(links))
    
    clean_links = []
    data2 = []
    for link in links:
        link = link.replace('.com//','.com/')
        if(link not in clean_links):
            clean_links.append(link)
            data2.append(CarFaxVehicleScrapper(link))
            
    #storing dealer data in Pandas Dataframes
    all_dealers = [x['dealer_info'] for x in data2]
    dealer_df = pd.DataFrame(all_dealers)
    
    #storing Car_description data in  Dataframe
    vin= [k['vin'] for k in data2]
    make=[k['make'] for k in data2]
    model=[k['model'] for k in data2]
    ext_color= [k['ext_color'] for k in data2]
    int_color= [k['int_color'] for k in data2]
    body_style= [k['body_style'] for k in data2]
    year= [k['year'] for k in data2]
    
    list_of_descriptions= list(zip(vin,make,model,ext_color,int_color,body_style,year))
    car_descriptions_df=  pd.DataFrame(list_of_descriptions, columns=['vin','make','model','ext_color','int_color','body_style','year'])
    
    #storing Vehicle_info data in  Dataframe
    mileage= [k['mileage'] for k in data2]
    location= [k['location'] for k in data2]
    v_info_list = list(zip(vin,mileage,location))
    v_info_df= pd.DataFrame(v_info_list, columns=['vin','mileage','location'])
    
    #storing Storing  drivetrain data in  Dataframe
    drive_type= [k['drive_type'] for k in data2]
    engine= [k['engine'] for k in data2]
    transmission= [k['transmission'] for k in data2]
    mpg= [k['mpg'] for k in data2]
    fuel= [k['fuel'] for k in data2]
    
    drive_train_list= list(zip(vin,drive_type,engine,transmission,mpg,fuel))
    drive_train_df= pd.DataFrame(drive_train_list, columns= ['vin','drive_type','engine', 'transmission', 'mpg', 'fuel'])
    
    #storing Price data in  Dataframe
    price= [x['price'] for x in data2]
    price_list= list(zip(vin,price))
    price_df= pd.DataFrame(price_list, columns=['vin', 'price'])
    
    
    #load into MongoDB
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Define the 'classDB' database in Mongo
    db = client.carfaxDB
    
    db.price_df.insert_many(price_df.to_dict('records'))
    
    db.driveTrain_df.insert_many(drive_train_df.to_dict('records'))
    db.vehicleInfo_df.insert_many(v_info_df.to_dict('records'))
    db.carDescriptions_df.insert_many(car_descriptions_df.to_dict('records')) 
    db.dealer_df.insert_many(dealer_df.to_dict('records'))