#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GrocerySub Streamlit Dashboard

Created on Thu Jun 11 21:20:58 2020

@author: chrki23
"""

### Package loading

import streamlit as st
# import st_state_patch

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

@st.cache
def lookup_loader (lookup_path = lookup_path):
    fileloader = open(lookup_path, 'rb')
    lookup_table = pickle.load(fileloader)
    fileloader.close()
    return lookup_table
    
    
vector_path = path + '/data/cleaned/final_vectors.kv'

@st.cache
def vector_loader (vector_path = vector_path):
    fname = get_tmpfile(vector_path)
    return KeyedVectors.load(fname, mmap = "r")


ingredients_path = path + '/data/cleaned/ingredients_used.data'

@st.cache
def ingredient_loader (ingredients_path = ingredients_path):
    fileloader = open(ingredients_path, 'rb')
    ingredients_used = pickle.load(fileloader)
    fileloader.close()
    return ingredients_used
    


### 

st.title('Hello world')

lookup_table = lookup_loader(lookup_path)
word_vectors = vector_loader(vector_path)


# category_input = st.selectbox(
#     'Choose a category:',
#     lookup_table.product_category.unique())

# category_input

# user_input = st.selectbox(
#     'Choose a product:',
#     lookup_table.name)

# user_input

user_input = st.multiselect(
    'Select me',
    lookup_table.name)

### Helper functions

# Display table with product info
def display_choice (user_input):
    missing_product = lookup_table[lookup_table.name == user_input]
    return missing_product.iloc[:,0:4]

# Move from choosing grocery product to target ingredient from curated list
def get_ingredient (user_input):
    input_ingredient = lookup_table.ingredient_match[lookup_table.name == user_input]
    return input_ingredient

# # Access most similar ingredients to target ingredient from word2vec
# def get_similar_ingredients (input_ingredient):
#     ing_formatted = []
#     ing_toplist = word_vectors.most_similar(input_ingredient)
#     for i in ing_toplist:
#         ing_formatted.append(i[0])
#     return ing_formatted

def similar_ingredients (ingredient, ingredients_used):
    top_raw = word_vectors.most_similar(ingredient, topn = 20)
    top = [x for x,y in top_raw if x in ingredients_used]
    if len(top) >= 10:
        return top[:10]
    else:
        return top
    
# Return the top product suggestions matching the most similar ingredients
def get_top_subs (similar_ingredients):
    sub_toplist = pd.DataFrame(columns = lookup_table.columns[0:4])
    for i in similar_ingredients:
        sub_toplist.append(lookup_table.iloc[:,0:4][lookup_table.ingredient == i], ignore_index = True)
    return sub_toplist


# def substitution_output():
    
#     # Print user input table
#     missing_product = display_choice(user_input)
    
#     # Match product to ingredient
#     input_ingredient = get_ingredient(user_input)
    
#     # Interact with word vectors
#     similar_ingredients = get_similar_ingredients(input_ingredient)
    
#     # Return similar products for top 3 ingredients
#     top_subs = get_top_subs(similar_ingredients)
    
#     return missing_product, similar_ingredients, top_subs

missing_product = display_choice(user_input)
st.write(missing_product)

# st.write(similar_ingredients)
# st.write(top_subs)
