#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:17:19 2020

@author: chrki23
"""

import os

path = os.getcwd()
print(path)

### Import grocery items and ingredients

import pickle

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
product_filtered = product_df[~product_df.product_category.isin(excluded_categories)]


# Create edited product list to improve matching

product_df['name_edit'] = product_df.name.str.lower()

# Remove numbers

import re
product_df['name_edit'] = product_df['name_edit'].apply(lambda x: re.sub(r'\d+', '', x))

# Filter punctuation

import string
table = str.maketrans('', '', string.punctuation)
product_df['name_edit'] = product_df.name_edit.apply(lambda x: x.translate(table))

# Strip leading whitespace

product_df['name_edit'] = product_df.name_edit.apply(lambda x: x.strip())

# # Tokenize and takg parts of speech with POS tagger

# import nltk
# from nltk.tokenize import word_tokenize

# product_df['name_edit'] = product_df.name_edit.apply(lambda x: word_tokenize(x))

# product_df['name_edit'] = product_df.name_edit.apply(lambda x: nltk.pos_tag(x))


# # Filter out POS eg. verbs except present participle eg. 'baking'

# excluded_tags = ['VB', 'VBD', 'VBN', 'VBP', 'VBZ', 'CC']
# def verb_remove (lst):
#     for i in list:
#         if i not in excluded_tags:
#             return i[1]
#         else:
#             return ''

# product_df['name_edit'] = product_df.name_edit.apply(lambda x: verb_remove(x))

# Prepare ingredients list

ingredient_list = [word.replace('_', ' ') for word in ingredients_used]


### Match products to ingredients

from fuzzywuzzy import process

fuzz_score = []

def fuzz_match (product_names, ingredient_list):
    for i in product_names:
        score = process.extractOne(i, ingredient_list)
        fuzz_score.append(score)
        
fuzz_match(product_df.name_edit, ingredient_list)

# Write out
fileloader = open(path + '/data/cleaned/fuzzymatch_scores.data', 'wb')
pickle.dump(fuzz_score, fileloader)
fileloader.close()

fuzz_df = pd.DataFrame.from_dict(fuzz_score)
fuzz_df.columns = ['ingredient', 'fuzz_score']

product_df = product_df.append(fuzz_df)


        
# def fuzz_match2 (product_names, ingredient_list):
#     for i in product_names:
#         scores = dict()
#         best_score = process.extractOne(i, ingredient_list)
        
#         scores['ingredient'] = best_score[0]
#         scores['fuzz_score'] = best_score[1]
        
#         fuzz_score.append(scores)

# import nltk

# jacc_score = pd.DataFrame(columns = ['ingredient', 'score'])

# def jacc_match (product_names, ingredient_list):
#     for i in product_names[:5]:
#         jd = pd.DataFrame(columns = ['ingredient', 'score'])
#         for count, j in enumerate(ingredient_list):
#             score = nltk.jaccard_distance(set(i), set(j))
#             jd.loc[count] = [j] + list(score)
#     min_score = jd[jd.score == jd.score.min()]
#     print(min_score)
#     jacc_score.append(min_score)
    
# test = jacc_match(product_df.name_edit, ingredients_used)
