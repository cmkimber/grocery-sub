#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Match grocery e-commerce product titles to ingredients

Created on Wed Jun 10 21:17:19 2020

@author: chrki23
"""

import os
import pickle

os.chdir('/Users/chrki23/Documents/Insight_Project')
path = os.getcwd()
print(path)

### Import grocery items and ingredients

fileloader = open(path + '/data/cleaned/ingredients_used.data', 'rb')
ingredients_used = pickle.load(fileloader)
fileloader.close()

fileloader = open(path + '/data/cleaned/grocery_items_v1.data','rb')
product_list = pickle.load(fileloader)
fileloader.close()


### Filter product list by product category

import pandas as pd

product_df = pd.DataFrame.from_dict(product_list)
excluded_categories = ['Household & Cleaning', 'Health & Beauty', 'Pet Care', 'Baby', 'Pharmacy', 'Eco-Friendly Household Cleaning Products', 'Other Animals']
product_filtered = product_df.copy()
product_filtered = product_filtered[~product_filtered.product_category.isin(excluded_categories)]


# Create edited product list to improve matching

product_filtered['name_edit'] = product_filtered.name.str.lower()

# Remove numbers

import re
product_filtered['name_edit'] = product_filtered['name_edit'].apply(lambda x: re.sub(r'\d+', '', x))

# Filter punctuation

import string
table = str.maketrans('', '', string.punctuation)
product_filtered['name_edit'] = product_filtered.name_edit.apply(lambda x: x.translate(table))

# Strip leading whitespace

product_filtered['name_edit'] = product_filtered.name_edit.apply(lambda x: x.strip())


# Prepare ingredients list

ingredient_list = [word.replace('_', ' ') for word in ingredients_used]


### Match products to ingredients

from fuzzywuzzy import process

fuzz_score = []

def fuzz_match (product_names, ingredient_list):
    for i in product_names:
        score = process.extractOne(i, ingredient_list)
        fuzz_score.append(score)
        
fuzz_match(product_filtered.name_edit, ingredient_list)

# Write out matches
fileloader = open(path + '/data/cleaned/fuzzymatch_scores.data', 'wb')
pickle.dump(fuzz_score, fileloader)
fileloader.close()

fuzz_df = pd.DataFrame.from_dict(fuzz_score)
fuzz_df.columns = ['ingredient', 'fuzz_score']

product_filtered = product_filtered.reset_index(drop = True)
lookup_table = pd.concat([product_filtered, fuzz_df], axis = 1)
lookup_table['ingredient'] = lookup_table['ingredient'].str.replace(' ', '_')

# Write out lookup table
fileloader = open(path + '/data/cleaned/lookup_table.data', 'wb')
pickle.dump(lookup_table, fileloader)
fileloader.close()

