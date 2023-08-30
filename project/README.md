## GrocerySub App Readme

The original Plotly Dash app code for running locally and on PythonAnywhere in 2020 was built for Python 3.7 with Pandas 1.0, Gensim 3.8 and Dash 1.12, and is launched from dashapp.py.

In 2023 I put the app back up on PythonAnywhere and had to adapt it to the package versions currently installed there (not enough disk space on a free account to install the necessary legacy package versions in a venv). The current version for PythonAnywhere is built for Python 3.7 with Pandas 1.3, Gensim 4.2 and Dash 2.4; each of those package upgrades required a coding change in the app for it to run correctly. These changes are reflected in dashapp_pyanywhere_current.py.

Changelog:
- Explicitly coerce ingredient contained in selected product from Pandas series to list (due to changes in Pandas' handling of string data)
- Add kwarg "positive" in KeyedVectors.most_similar call (due to changes in Gensim 4)
- Change callback code structure to include kwargs etc. (due to the addition of flexible callbacks and other changes in callback structure in Dash 2.0)
