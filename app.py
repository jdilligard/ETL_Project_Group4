from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import carfax_scraper
import pymongo

app = Flask(__name__)

@app.route("/scrape")
def scrape():
    carfax_data= carfax_scraper.scrape_info()


if __name__=="__main__":
    app.run(debug=True)