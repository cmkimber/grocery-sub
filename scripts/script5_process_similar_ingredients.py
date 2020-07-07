#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper function to select similar ingredients from similar words

Created on Wed Jun 10 20:37:21 2020

@author: chrki23
"""


from gensim import Word2Vec, KeyedVectors

### Filter model most similar list for ingredients in master list

def similar_ingredients (ingredient, model, ingredients_used):
    top_raw = model.wv.most_similar(ingredient, topn = 20)
    top = [(x,y) for x,y in top_raw if x in ingredients_used]
    if len(top) >= 10:
        return top[:10]
    else:
        return top
    

