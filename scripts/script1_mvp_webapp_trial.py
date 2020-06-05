#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 22:35:58 2020

@author: chrki23
"""

import pickle
from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile
import numpy as np
import pandas as pd

# Load webshop products and matched ingredients
file = open('/Users/chrki23/Documents/Insight_Project/data/cleaned/products_matched_scores_filt.data', 'rb')
product_table = pickle.load(file)
file.close()

# Load word2vec vectors (KeyedVectors load might be more efficient?)
fname = get_tmpfile("/Users/chrki23/Documents/Insight_Project/data/cleaned/vectors.kv")
word_vectors = KeyedVectors.load(fname, mmap = 'r')


# Move from choosing grocery product to target ingredient from curated list
def get_ingredient (user_input):
    input_ingredient = product_table.ingredient_match[product_table.name == user_input]
    return input_ingredient

# Access most similar ingredients to target ingredient from word2vec
def get_similar_ingredients (input_ingredient):
    ing_formatted = []
    ing_toplist = word_vectors.most_similar(input_ingredient)
    for i in ing_toplist:
        ing_formatted.append(i[0])
    return ing_formatted

# Return the top product suggestions matching the most similar ingredients
def get_top_subs (similar_ingredients):
    sub_toplist = []
    for i in similar_ingredients:
        sub_toplist.extend(product_table.name[product_table.ingredient_match == i].values.tolist())
    return sub_toplist


# Comes from input textbox in flask app
test = 'vegetable oil'

def substitution_output():
    
    # Pull input
    #user_input = request.args.get('user_input')
    user_input = test
    
    # Match product to ingredient
    input_ingredient = get_ingredient(user_input)
    
    # Interact with word vectors
    similar_ingredients = get_similar_ingredients(input_ingredient)
    
    # Return similar products for top 3 ingredients
    top_subs = get_top_subs(similar_ingredients)
    
    return input_ingredient, similar_ingredients, top_subs
    

# Test that the output is working before implementing code in Flask
output1, output2, output3 = substitution_output()
print(output1)
print(output2)
print(output3)

