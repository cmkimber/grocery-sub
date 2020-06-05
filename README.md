# GrocerySub

GrocerySub is a tool that leverages information on food ingredient use cases found in online recipes to improve the scope or quality of substitution suggestions during online shopping.

At present, GrocerySub is a work in progress. It currently combines online grocery product information from the Metro webshop with a curated master ingredient list and recipe ingredients sourced from the simplified-recipes-1M dataset found at https://dominikschmidt.xyz/simplified-recipes-1M/.

At its heart, GrocerySub is using a word embedding model trained on the recipe ingredient lists using word2vec. The cosine similarities between ingredients are used to estimate the most similar ingredients in terms of use case.

The pipeline works as follows:

  1. Import grocery product name from webshop
  2. Match product names to curated master ingredient list using fuzzywuzzy
  3. Find similar ingredients for a target ingredient using word2vec word embeddings.
  4. For similar ingredients, find matching products using the fuzzywuzzy output from step 2.
  5. Output suggested substitute products for the input product

## Current status

GrocerySub currently exists as a minimal Flask webapp. Data is hosted locally and so is not currently useable online.

## Prequisites

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Running the webapp

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Acknowledgments

- Lorem ipsum dolor sit amet.
