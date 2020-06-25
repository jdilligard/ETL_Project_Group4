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
import pymongo
from sqlalchemy import create_engine
from Scrapper import *



def pandas_to_mongo(dict):
    print('Im doing the mongo thing')
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define the 'classDB' database in Mongo
    db = client.carfaxDB
    price_df = dict['price']
    drive_train_df = dict['drive_train']
    v_info_df = dict['vehicle_info']
    car_descriptions_df = dict['car_descriptions']
    dealer_df = dict['dealer']
    
    db.price_df.insert_many(price_df.to_dict('records'))
    db.driveTrain_df.insert_many(drive_train_df.to_dict('records'))
    db.vehicleInfo_df.insert_many(v_info_df.to_dict('records'))
    db.carDescriptions_df.insert_many(car_descriptions_df.to_dict('records'))
    db.dealer.insert_many(dealer_df.to_dict('records'))
    print('I did the mongo thing')
    return



def pandas_to_postgres(dict):
    engine = create_engine('sqlite://', echo=False)
    print('I did the postgres thing')
    




