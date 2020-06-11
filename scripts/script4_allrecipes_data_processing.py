#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:25:18 2020

@author: chrki23
"""

import os

path = os.getcwd()
print(path)

import pandas as pd

data = pd.read_json(path + "/data/raw/allrecipes-recipes.json", lines = True)

# Visual inspection of the JSON shows that *many* recipes come from one author and do not add any information (how to top a pizza). Delete.
data_no_sausage = data[data.author != 'The Kitchen at Johnsonville Sausage']
data = data_no_sausage

ingredients = data.ingredients.copy()
instructions = data.instructions.copy()

# ingredients_test= ingredients[:10]

# ingredients_test = [[entry.lower() for entry in recipe] for recipe in ingredients_test]


### Ingredient processing with NLTK
#Steps

# Set to lower case

ingredients = [[entry.lower() for entry in recipe] for recipe in ingredients]

# Remove numbers

import re
ingredients = [[re.sub(r'\d+', '', entry) for entry in recipe] for recipe in ingredients]


# Filter punctuation

import string
table = str.maketrans('', '', string.punctuation)
ingredients = [[entry.translate(table) for entry in recipe] for recipe in ingredients]

# Strip leading whitespace

ingredients = [[entry.strip() for entry in recipe] for recipe in ingredients]

# Tokenize and tag parts of speech with pos tagger 

import nltk

nltk.download('punkt')
nltk.download('averaged_perception_tagger')
from nltk.tokenize import word_tokenize

ingredients = [[word_tokenize(entry) for entry in recipe] for recipe in ingredients]


ingredients_tagged = [[nltk.pos_tag(entry) for entry in recipe] for recipe in ingredients]

# save out tagged list
# import pickle
# filehandler = open('/Users/chrki23/Documents/Insight_Project/data/cleaned/ingredient_tags.data', 'wb')
# pickle.dump(ingredients_tagged, filehandler)


# Filter out POS eg. verbs except present participle eg. 'baking'

excluded_tags = ['VB', 'VBD', 'VBN', 'VBP', 'VBZ', 'CC']
ingredients_filtered = [[[t for t in tags if t[1] not in excluded_tags] for tags in recipe]for recipe in ingredients_tagged]

# Lemmatize

from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def singularize_nouns (t):
    if t[1] in ['NNPS', 'NNS']:
        return lemmatizer.lemmatize(t[0], pos = 'n')
    else:
        return t[0]

ingredients_filtered = [[[singularize_nouns(t) for t in tags] for tags in recipe] for recipe in ingredients_filtered]


# Filter stop words

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

ingredients_filtered = [[[w for w in entry if not w in stop_words] for entry in recipe] for recipe in ingredients_filtered]


# Omit weights and measures

units = ['ounce', 'ounces', 'cups', 'cup', 'teaspoon', 'tablespoon', 'tablespoons', 'teaspoons', 'c', 'g', 'v', 'tbsp', 'x', 'ml', 'lb', 'tbs', 'oz', 'pkg', 'large', 'small', 'tsp', 'inch', 'grams', 'quarts', 'lbs', 'can', 'cube', 'whole', 'or', 'pieces', 'piece', 'chopped', 'shredded', 'diced', 'fresh', 'crushed', 'tsp', 'package', 'kg', 'kilogram', 'gallon', 'degree', 'degrees', 'temperature', 'hot', 'warm', 'cold', 'boiling', 'lukewarm', 'f', 'c','slice', 'sliced', 'fresh', 'freshly', 'pound', 'pounds', 'thin', 'thinly', 'thick', 'thickly', 'coarsely', 'finely', 'jar', 'strip', 'strips', 'cut', 'peeled', 'wedge', 'bitesize', 'according', 'direction', 'optional', 'bite', 'size', 'half', 'pinch', 'dash', 'eg', 'frozen', 'thawed', 'recipe', 'fat', 'quart', 'quarts', 'pint', 'pints', 'splash', 'container', 'fried', 'cooked', 'uncooked', 'boiled', 'reduced', 'drained', 'water', 'one', 'washed', 'rinsed', 'pitted', 'head', 'tube', 'fluid', 'fl', 'preferably', 'bottle', 'diagonally', 'crosswise', 'lengthwise', 'torn', 'serving', 'bunch', 'halved', 'part', 'quartered', 'available', 'grocery', 'first', 'andor', 'substitution', 'bar']

ingredients_clean = [[[w for w in entry if not w in units] for entry in recipe] for recipe in ingredients_filtered]

# Omit brands

ingredients_clean = [[[w for w in entry if not ['®', '™'] in w] for entry in recipe] for recipe in ingredients_clean]

# Remove empty lists

ingredients_clean = [[entry for entry in recipe if entry != [] ]for recipe in ingredients_clean]

filehandler = open(path + '/data/cleaned/ingredients_cleaned.data', 'wb')
pickle.dump(ingredients_clean, filehandler)
