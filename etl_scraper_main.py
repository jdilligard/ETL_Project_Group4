#!/usr/bin/env python
# coding: utf-8


#This is the etl scraper for team 4. It goes to Carfax.com and searches for Jeep Cherokees in the Dallas Area.


#Import the important libraries
from time import time,sleep
from random import randint
from IPython.core.display import clear_output
from requests import get
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re 

from Scrapper import *
from pandas_to_x import *



#This is the url for the search that we are doing at Carfax.com
url = 'https://www.carfax.com/Used-Jeep-Cherokee-Dallas-TX_w371_c18864'



#This function goes to the carfax page and scrapes all of the pertinent info such as location, VIN, color etc. 
#After scraping the info, the info is placed in to several pandas data frames that correlate to our ERD database structure
#The dataframes are place into a dictionary called 'dict' and returned
dict = scrapper_to_pandas(url)




dict.keys()



#This function takes the 'dict' function and loads the data into several data tables in MongoDB.  
pandas_to_mongo(dict)

