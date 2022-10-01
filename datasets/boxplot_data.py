### ------ Importações ------ ###
### ------ From dash ------ ###
# from dash import dcc, html, dash_table
# import dash_bootstrap_components as dbc

### ------ Third part ------ ###
import pandas as pd


### ------ Python ------ ###
import os



### ------ loading ------ ###
script_dir = os.getcwd()


df_data_set_info = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'datasets/boxplots_data_sets/df_data_set_info.csv')))

df_data_set = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'datasets/boxplots_data_sets/df_data_set.csv')))

df_results = pd.read_csv(os.path.normcase(os.path.join(script_dir, 'datasets/boxplots_data_sets/df_results.csv')))


















#
