#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:35:51 2020

@author: chrki23
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import re

webshop_domain = 'https://metro.ca/en/'
path = 'online-grocery/search'
url = (webshop_domain + path)

# driver = webdriver.Chrome()
# driver.get(url)
# driver.find_element_by_css_selector("button[class = 'ipdetection--close p__close']").click()
# page = driver.page_source
# soup = BeautifulSoup(page, features = 'html.parser')
# driver.close()

# item_classes = "products-tile-list__tile"
# item_list = soup.find_all('div', class_ = item_classes[0])



    
# first_item = item_list[7]
    
# #brand = first_item.find('span', class_ = 'pt-brand').text

# name = first_item.find('div', class_ = 'pt-title').text
# sale_unit = first_item.find('span', class_ = 'pt-weight').text

# product_category = first_item.find('div', class_ = re.compile("^tile-product item-addToCart")).attrs['data-product-category']

# image_link = first_item.find('picture', class_ = 'tile-product__top-section__visuals__img-product defaultable-picture').find('source').attrs['srcset'].split(',')[0]

# print(name, sale_unit, product_category, image_link)


def get_max_pagenum (soup):
    pc = soup.find('span', class_ = 'ppn--short').text
    split_pc = pc.split("/")
    return int(split_pc[1])


import time
import numpy as np

driver = webdriver.Chrome()
driver.get(url)

driver.find_element_by_css_selector("button[class = 'ipdetection--close p__close']").click()

items = []

pageCounter = 0

soup = BeautifulSoup(driver.page_source, features = 'html.parser')
maxPageCount = get_max_pagenum(soup)

while(pageCounter < maxPageCount):
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, features = 'html.parser')
    item_containers = soup.find_all('div', class_ = "products-tile-list__tile")
    for item in item_containers:
        
        single_item = dict()
        
        single_item['name'] = item.find('div', class_ = 'pt-title').text
        
        if item.find('span', class_ = 'pt-brand') is None:
            single_item['brand'] = np.nan
        else:
            single_item['brand'] = item.find('span', class_ = 'pt-brand').text
        
        if item.find('span', class_ = 'pt-weight').text == "":
            single_item['sale_unit'] = np.nan
        else:
            single_item['sale_unit'] = item.find('span', class_ = 'pt-weight').text
               
        single_item['product_category'] = item.find('div', class_ = re.compile("^tile-product item-addToCart")).attrs['data-product-category']
        
        if item.find('picture', class_ = 'tile-product__top-section__visuals__img-product defaultable-picture').find('source') is None:
            single_item['image_link'] = np.nan
        else:
            single_item['image_link'] = item.find('picture', class_ = 'tile-product__top-section__visuals__img-product defaultable-picture').find('source').attrs['srcset'].split(',')[0]
        
        items.append(single_item)
        
    driver.find_element_by_css_selector("a[aria-label='Next']").click()
    pageCounter +=1
    print(pageCounter)
    
driver.close


import pandas as pd

items_df = pd.DataFrame.from_dict(items)

import pickle
filehandler = open('/Users/chrki23/Documents/Insight_Project/data/cleaned/grocery_items_v1.data', 'wb')
pickle.dump(items, filehandler)