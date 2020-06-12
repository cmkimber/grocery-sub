#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 00:52:33 2020

@author: chrki23
"""

import streamlit as st

import pandas as pd
import pickle
import os


from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

### Setup

os.chdir('/Users/chrki23/Documents/Insight_Project')
path = os.getcwd()


### File Loading

lookup_path = path + '/data/cleaned/lookup_table.data'
fileloader = open(lookup_path, 'rb')
lookup_table = pickle.load(fileloader)
fileloader.close()


vector_path = path + '/data/cleaned/final_vectors.kv'
fname = get_tmpfile(vector_path)
word_vectors = KeyedVectors.load(fname, mmap = "r")


ingredients_path = path + '/data/cleaned/ingredients_used.data'
fileloader = open(ingredients_path, 'rb')
ingredients_used = pickle.load(fileloader)
fileloader.close()


### Helper functions

def display_choice (user_input):
    missing_product = lookup_table[(lookup_table.name.isin(user_input))]
    return missing_product.iloc[:,0:4]

def get_ingredient (user_input):
    input_ingredient = lookup_table.ingredient[(lookup_table.name.isin(user_input))]
    return input_ingredient

def get_similar_ingredients (ingredient, ingredients_used):
    top_raw = word_vectors.most_similar(ingredient, topn = 20)
    top = [x for x,y in top_raw if x in ingredients_used]
    if len(top) >= 10:
        return top[:10]
    else:
        return top
    
def get_top_subs (similar_ingredients):
    sub_toplist = []
    for i in similar_ingredients:
        sub_toplist.extend(lookup_table[lookup_table.ingredient == i].values.tolist())
    if len(sub_toplist) > 20:
        return pd.DataFrame(sub_toplist[:20], columns = lookup_table.columns)
    else:
        return pd.DataFrame(sub_toplist, columns = lookup_table.columns)


# Display results

st.title('GrocerySub')

# Temporary, fixed in pipeline now
lookup_table['ingredient'] = lookup_table['ingredient'].str.replace(' ', '_')

st.write('Select a webshop product')
user_input = st.multiselect('Choose product:', lookup_table.name)

missing_product = display_choice(user_input)
st.write(missing_product)

input_ingredient = get_ingredient(user_input)

st.write('Similar ingredients')
similar_ingredients = get_similar_ingredients(input_ingredient, ingredients_used)
st.write(similar_ingredients)

st.write('Possible substitution suggestions')
top_subs = get_top_subs(similar_ingredients)
st.write(top_subs.iloc[:,0:4])