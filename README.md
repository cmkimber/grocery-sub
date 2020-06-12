# GrocerySub

GrocerySub is a tool that leverages information on food ingredient use cases found in online recipes to improve the scope or quality of substitution suggestions during online shopping.

At present, GrocerySub is a work in progress. It currently combines online grocery product information from the Metro webshop with a dataset of recipes found on https://archive.org/details/recipes-en-201706 that were scraped from Allrecipes in 2017. The full dataset is ~225K recipes but >125K are corporate spam which GrocerySub does not use. Future plans for GrocerySub include the addition of more data from other sources.

At its heart, GrocerySub is using a word embedding model trained on the recipe instructions using word2vec. Ingredients are identified by preprocessing the ingredient lists from the recipe dataset using NLTK and identifying n-grams using a gensim.Phrases model. The instructions are processed to include n-grams before training the word embedding model. Cosine similarities between ingredients are used to estimate the most similar ingredients in terms of use case.

The pipeline works as follows:

  1. Import grocery product name from webshop
  2. Match product names to preprocessed master ingredient list using fuzzywuzzy
  3. Find similar ingredients for a target ingredient using word2vec word embeddings.
  4. For similar ingredients, find matching products using the fuzzywuzzy output from step 2.
  5. Output suggested substitute products for the input product

## Current status

GrocerySub currently exists as a dashboard in Streamlit; performance is not optimal when querying the large product table. Data is hosted locally and so is not currently useable online.

Scripts used to import and preprocess the data, to fit the model and to work with the webshop scraping and resulting data are available.

## Prequisites

nltk

gensim: both word2vec and Phrases

Streamlit: to implement the dashboard

Selenium: for webshop scraping

Beautiful Soup

fuzzywuzzy

## Running the dashboard

The prototype dash currently is run from streamtoy.py. Upgrades and online functionality forthcoming.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Acknowledgments

- Lorem ipsum dolor sit amet.
