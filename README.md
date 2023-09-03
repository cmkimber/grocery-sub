# GrocerySub

## Update: September 2023

GrocerySub was built as an integral part of my time as an Insight Data Science Fellow in the now-defunct Toronto programme, during its final session in spring/summer 2020. It was built (from ideation through to functional public web app) in 4 weeks. I recently made small updates to allow it to run on a current-spec PythonAnywhere instance but otherwise it remains as it was at the end of the 4 week development cycle.

## What is GrocerySub?

GrocerySub is a tool that leverages information on food ingredient use cases found in online recipes to improve the scope or quality of substitution suggestions during online shopping. GrocerySub is not designed to make a single substitution recommendation, or even to replace other types of substitution recommenders. Rather, it aims to broaden the scope of substitution suggestions by surfacing products that may fill the 'role' of a missing product when the customer is cooking. A dashboard to explore the recommendations GrocerySub can produce is found online at https://cmkimber.pythonanywhere.com/. The dashboard was built using Plotly Dash.

GrocerySub currently combines online grocery product information from the Metro webshop with a dataset of recipes found on https://archive.org/details/recipes-en-201706 that were scraped from Allrecipes in 2017. The full dataset is ~225K recipes but >125K are corporate spam which GrocerySub does not use. Future plans for GrocerySub include the addition of more data from other sources.

At its heart, GrocerySub is using a word embedding model trained on the recipe instructions using word2vec. Ingredients are identified by preprocessing the ingredient lists from the recipe dataset using NLTK and identifying n-grams using a gensim.Phrases model. The instructions are processed to include n-grams before training the word embedding model. Cosine similarities between ingredients are used to estimate the most similar ingredients in terms of use case.

## How does the GrocerySub dash work?

The pipeline works as follows:

  1. Import grocery product name from webshop
  2. Match product names to preprocessed master ingredient list using fuzzywuzzy
  3. Find similar ingredients for a target ingredient using word2vec word embeddings.
  4. For similar ingredients, find matching products using the fuzzywuzzy output from step 2.
  5. Output suggested substitute products for the input product

## Prequisites

For the dashboard:

Dash,
gensim.KeyedVectors

For preparing the data and modelling:

nltk,
gensim: both Phrases and Word2Vec,
Selenium,
Beautiful Soup,
fuzzywuzzy

## Running the dashboard

When you enter the dash at https://cmkimber.pythonanywhere.com, you begin by choosing a grocery product category. These categories are filtered to remove those which do not contain products typically used as recipe ingredients. Such products will not produce meaningful substitutions based on ingredient use cases.

GrocerySub intentionally surfaces both similar ingredients and product suggestions for a given user search. This is done because the product database from a single webshop is intended as an example implementation and does not represent a comprehensive selection of grocery items. This can be especially relevant for speciality or regional ingredients. By showing the similar ingredients found 'under the hood', the potential impact of GrocerySub outside of the example webshop product space is more readily seen.

Product suggestions in GrocerySub are currently made by returning all products matching to the most similar ingredient, followed by those matching the 2nd most similar, etc. up until 20 products are shown. User options for controlling the algorithm that returns product suggestions is a feature targeted for future development.

## Why I built GrocerySub

GrocerySub was conceived as a way to learn about NLP, word embedding, webscraping and recommendation system-building.

The true motivation for GrocerySub, however, came from experiences my partner and I had when we started shopping for groceries online during the COVID-19 pandemic. We often start with a recipe and then shop for ingredients. It frustrated us a lot when an item was missing and no substitute was provided since many ingredients could often fill its place but no ingredient could mean a big hole in the recipe and another shopping trip.

GrocerySub is intended to help expand the scope of ingredient substitutions to include products that are often used in the same way as the out-of-stock product when cooking. Rather than standing alone, it would act as part of a recommendation pipeline for human-in-the-loop substitution systems, either through a webshop or Instacart-style service. The core of GrocerySub, using ingredients rather than products, could also provide a valuable service to home cooks looking for alternatives when an ingredient is unavailable in various circumstances.

## Acknowledgments

Thank you to all my wonderful fellow fellows in the Insight Data Science Toronto 20B, the Insight staff, and my partner for putting up with me being lost to Zoom and late nights coding!
