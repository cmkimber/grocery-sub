from flask import Flask, render_template, request
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

# Define custom functions (not loading from package at this stage)
def get_ingredient (user_input):
    input_ingredient = product_table.ingredient_match[product_table.name == user_input]
    return input_ingredient

def get_similar_ingredients (input_ingredient):
    ing_formatted = []
    ing_toplist = word_vectors.most_similar(input_ingredient)
    for i in ing_toplist:
        ing_formatted.append(i[0])
    return ing_formatted

def get_top_subs (similar_ingredients):
    sub_toplist = []
    for i in similar_ingredients:
        sub_toplist.extend(product_table.name[product_table.ingredient_match == i].values.tolist())
    return sub_toplist

# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
    return render_template('index.html')  # render a template

@app.route('/output')
def substitution_output():
#
       # Pull input
       user_input =request.args.get('user_input')

       # Case if empty
       if user_input == "":
           return render_template("index.html",
                                  my_input = some_input,
                                  my_form_result = "Empty")
       else:
           # Match product to ingredient
           input_ingredient = get_ingredient(user_input)

           # Interact with word vectors
           similar_ingredients = get_similar_ingredients(input_ingredient)

           # Return similar products for top 3 ingredients
           top_subs = get_top_subs(similar_ingredients)

           some_output="yeay!"
           some_number=3
           some_image="giphy.gif"
           return render_template("index.html",
                              my_input=user_input,
                              my_output=', '.join(top_subs),
                              my_number=some_number,
                              my_img_name=some_image,
                              my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/
