# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:08:17 2021

@author: Admin
"""
import requests
from flask import Flask, jsonify, request
import re
import sys
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def url_scrape():
    try:
        outbreakList=[]
        page_no = request.args.get("page")
        url = 'https://www.who.int/emergencies/disease-outbreak-news/'+str(page_no)
        webpage = requests.get(url)
        soup = BeautifulSoup( webpage.text , 'html.parser')
        tags = [td.find(class_='full-title') for td in soup.find_all(class_="sf-list-vertical__title" )]
        for links in soup.find_all(class_="sf-list-vertical__item"):
            response={}
            outbreak_link =links.find_all('a',href=True) 
            article_link=links.find_all('span') 
            outbreak_date =str(article_link[2].get_text()).replace("|","")
            try:
                outbreak_info = re.sub('ｰ', '–', str(article_link[3].get_text()))
                outbreak_info = re.sub('-', '–', outbreak_info)
            except IndexError:
                outbreak_info = ""
            outbreak_details = outbreak_info.rsplit('–',1)
            try:
                outbreak_country = outbreak_details[1]
            except IndexError:
                outbreak_country = "Not Available"
            outbreak_info = outbreak_details[0]
            outbreak_details = links['href']
            response['outbreak']=outbreak_info.strip()
            response['outbreak_date']=outbreak_date.strip()
            response['outbreak_information']=outbreak_details
            response['outbreak_origin']=outbreak_country.strip()
            outbreakList.append(response)
        
        return jsonify(outbreakList)
    except:
        return sys.exc_info()[0]

if __name__ == '__main__':
    app.run(debug = False)
    
    
    
   

