#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 17:42:25 2020

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


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))



### Process instructions

instructions_processed = [[entry.lower() for entry in recipe] for recipe in instructions]


import string
table = str.maketrans('', '', string.punctuation)
instructions_processed = [[entry.translate(table) for entry in recipe] for recipe in instructions_processed]

instructions_processed = [[word_tokenize(entry) for entry in recipe] for recipe in instructions_processed]

instructions_tagged = [[nltk.pos_tag(entry) for entry in recipe] for recipe in instructions_processed]

# Save out tagged instructions
import pickle
filehandler = open('/Users/chrki23/Documents/Insight_Project/data/cleaned/instruction_tags.data', 'wb')
pickle.dump(instructions_tagged, filehandler)

# Lemmatize

nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def singularize_nouns (t):
    if t[1] in ['NNPS', 'NNS']:
        return lemmatizer.lemmatize(t[0], pos = 'n')
    else:
        return t[0]

instructions_clean = [[[singularize_nouns(t) for t in tags] for tags in recipe] for recipe in instructions_tagged]

# Save out clean instructions

filehandler = open('/Users/chrki23/Documents/Insight_Project/data/cleaned/instruction_clean.data', 'wb')
pickle.dump(instructions_clean, filehandler)

### Fit gensim phrasing model to ingredients

from gensim.models.phrases import Phrases, Phraser 

# sentence_stream = [[[token.lower() for token in word_tokenize(entry) if token not in stop_words and token.isalpha()] for entry in recipe] for recipe in instructions]

# flattened_stream = [item for sublist in sentence_stream for item in sublist]

# bigrams = Phrases(flattened_stream, min_count = 5, threshold = 10, delimiter = b'_')

ingredient_stream = [item for sublist in ingredients_clean for item in sublist]

bigram = Phrases(ingredient_stream, min_count = 10, threshold = 1, delimiter = b'_')

bigram_phraser = Phraser(bigram)
bigram_tokens = bigram_phraser[ingredient_stream]

trigram = Phrases(bigram_tokens, min_count = 10, threshold = 1)


### Apply n-gram models to instruction text

instructions_bi = [[bigram[entry] for entry in recipe] for recipe in instructions_clean]

instructions_tri = [[trigram[entry] for entry in recipe] for recipe in instructions_clean]

# Save out formatted instructions

filehandler = open(path + '/data/cleaned/instructions_ngrammed.data', 'wb')
pickle.dump(instructions_tri, filehandler)


