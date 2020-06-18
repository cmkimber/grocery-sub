#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 23:33:22 2020

@author: chrki23
"""

import os
import pickle

os.chdir('/Users/chrki23/Documents/Insight_Project')
path = os.getcwd()
print(path)

## Load ingredient and instruction data

fileloader = open(path + '/data/cleaned/ingredients_cleaned.data', 'rb')
ingredients_cleaned = pickle.load(fileloader)
fileloader.close()

fileloader = open(path + '/data/cleaned/instructions_ngrammed.data', 'rb')
instruction_ngram = pickle.load(fileloader)
fileloader.close()


### Try word2vec models to n-gram processed instructions

instruction_stream = [item for sublist in instruction_ngram for item in sublist]

from gensim.models import Word2Vec

# model1 = Word2Vec(instruction_stream, min_count = 5, size = 100, workers = 3, window = 5, sg = 0)

# model2 = Word2Vec(instruction_stream, min_count = 5, size = 300, workers = 3, window = 5, sg = 0)

# # Currently the winner
# model3 = Word2Vec(instruction_stream, min_count = 5, size = 300, workers = 3, window = 5, sg = 1)

# # Currently a contender
# model4 = Word2Vec(instruction_stream, min_count = 5, size = 300, workers = 3, window = 20, sg = 0)

# model5 = Word2Vec(instruction_stream, min_count = 5, size = 300, workers = 3, window = 20, sg = 1)


model = Word2Vec(instruction_stream, min_count = 5, size = 300, workers = 3, window = 5, sg = 1)


# Save out vectors from word2vec model

# from gensim.test.utils import get_tmpfile
# from gensim.models import KeyedVectors

# fname = get_tmpfile(path + '/data/cleaned/final_vectors.kv')
# model.wv.save(fname)

model.wv.save(path + '/data/cleaned/final_vectors_2.kv')

### Work with the ingredients list format

# Convert ingredients to true n-gram format
ingredients_ngram = [[("_".join(entry)) for entry in recipe] for recipe in ingredients_cleaned]

# Find the unique ingredients from across all recipes
ingredients_flat = [item for sublist in ingredients_ngram for item in sublist]
ingredients_set = set(ingredients_flat)
ingredients_unique = list(ingredients_set)

instructions_flat = [item for sublist in instruction_stream for item in sublist]

# Ingredients_used is the basis of the key to match to products
ingredients_used = list(ingredients_set.intersection(set(instructions_flat)))

# Save out ingredients used

fileloader = open(path + '/data/cleaned/ingredients_used.data', 'wb')
pickle.dump(ingredients_used, fileloader)
fileloader.close()
