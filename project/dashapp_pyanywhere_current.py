import dash
from dash import dcc
from dash import html
from dash import Input, Output, State, callback

import os
import pickle
import pandas as pd

from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

# Load in data

os.chdir('/Users/chrki23/Documents/Insight_Project')
path = os.getcwd()

fileloader = open(path + '/data/cleaned/lookup_table.data', 'rb')
lookup_table = pickle.load(fileloader)
fileloader.close()

fileloader = open(path + '/data/cleaned/ingredients_used.data', 'rb')
ingredients_used = pickle.load(fileloader)
fileloader.close()

fname = get_tmpfile(path + '/data/cleaned/final_vectors.kv')
word_vectors = KeyedVectors.load(fname, mmap = "r")

lookup_table['search_name'] = lookup_table[['name', 'brand', 'sale_unit']].fillna('').agg(', '.join ,axis = 1)
lookup_table['ingredient'] = lookup_table['ingredient'].str.replace(' ', '_')

available_categories = lookup_table['product_category'].unique()
available_products = lookup_table['search_name']

## Helper Functions

def get_ingredient (user_input):
    input_ingredient = lookup_table.ingredient[lookup_table.search_name == user_input]
    input_ingredient = input_ingredient.tolist()
    return input_ingredient

def get_similar_ingredients (ingredient, ingredients_used):
    top_raw = word_vectors.most_similar(positive = ingredient, topn = 20)
    top = [x for x,y in top_raw if x in ingredients_used]
    if len(top) >= 10:
        return top[:10]
    else:
        return top

def get_top_subs (similar_ingredients):
    sub_toplist = []
    for i in similar_ingredients:
        sub_toplist.extend(lookup_table[lookup_table.ingredient == i].values.tolist())
    if len(sub_toplist) > 20:
        return pd.DataFrame(sub_toplist[:20], columns = lookup_table.columns)
    else:
        return pd.DataFrame(sub_toplist, columns = lookup_table.columns)

def generate_ingredient_table(list, max_rows = 10):
    ingredient_df = pd.DataFrame(list)
    return html.Table([
        html.Thead(
            html.Tr([html.Th("Ingredient")])
        ),
        html.Tbody([
            html.Tr([
                html.Td(ingredient_df.iloc[i])
            ]) for i in range(min(len(list), max_rows))
        ])
    ])

formatted_colnames = {'name': 'Product Name', 'brand': 'Brand', 'sale_unit': 'Units', 'product_category': 'Product Category'}
def generate_output_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(formatted_colnames[col]) for col in dataframe.columns[:4]])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns[:4]
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

### App layout

app.layout = html.Div([
    html.H1('GrocerySub',
            style = {
                'textAlign': 'center'
            }
    ),
    html.Div(children = '''
        GrocerySub takes a grocery webshop product as input and returns suggested substitue ingredients and products.
        '''),
    html.Div([
        html.H3('Choose a product category:'),
        dcc.Dropdown(
            id = 'category',
            options = [{'label': i, 'value': i} for i in available_categories],
            value = 'Enter Category'),
            ],
        style = {'width': '48%'},
    ),
    html.Div([
        html.H3('Choose a product:'),
        dcc.Dropdown(
            id = 'product'),
        ],
        style = {'width': '48%'},
    ),
    html.Hr(),
    html.Div([
        html.H5('Click to see suggestions:'),
        html.Button('Submit', id = 'submit_button', n_clicks = None),
        ],
        style = {'textAlign': 'center'},
    ),
    html.Hr(),
    html.H4('Possible ingredient substitutions:'),
    html.Div(id = 'ingredient_output'),
    html.Hr(),
    html.H4('Possible product substitutions:'),
    html.Div(id = 'product_output')
])

### Input-output management

@callback(
    Output(component_id = 'product', component_property = 'options'),
    Input(component_id = 'category', component_property = 'value')
)
def set_product_options(selected_category):
    return[{'label': i, 'value': i} for i in available_products[lookup_table['product_category'] == selected_category]]

@callback(
    output = [Output(component_id = 'ingredient_output', component_property = 'children'),
    Output(component_id = 'product_output', component_property = 'children')],
    inputs = dict(n_clicks = Input(component_id = 'submit_button', component_property = 'n_clicks'),
    product_info = State(component_id = 'product', component_property = 'value'))
)
def output_return(n_clicks, product_info):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        input_ingredient = get_ingredient(product_info)

        similar_ingredients = get_similar_ingredients(input_ingredient, ingredients_used)

        top_subs = get_top_subs(similar_ingredients)

        return generate_ingredient_table(similar_ingredients), generate_output_table(top_subs)


if __name__ == '__main__':
    app.run_server(debug = True)
