#!/usr/bin/env python3

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html, State
import pickle
from model.peptide_reader_ml_model import amino_acid_features
import argparse
import logging
import socket
import sys

# -------------------------
# Logging setup
# -------------------------

parser = argparse.ArgumentParser(
    description="Run peptide sequence reader dashboard"
)

parser.add_argument(
    '-l', '--loglevel',
    required=False,
    default='WARNING',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help='Set log level'
)

args = parser.parse_args()

format_str = (
    f'[%(asctime)s {socket.gethostname()}] '
    '%(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
)

logging.basicConfig(level=args.loglevel, format=format_str)


# -------------------------
# Load data and model
# -------------------------

try:
    df = pd.read_csv('peptide_list_expanded.csv')

    with open('peptide_category_pipeline.pkl', 'rb') as f:
        peptide_model = pickle.load(f)

except FileNotFoundError:
    logging.error("File not found. Exiting.")
    sys.exit(1)


# -------------------------
# Dash app
# -------------------------

app = Dash()

app.layout = dbc.Container([
    dbc.Row([
        html.Div("Peptide Sequence Reader", className="text-primary text-center fs-3")
    ]),
    dbc.Row([
        dag.AgGrid(
            rowData=df.to_dict('records'),
            columnDefs=[{"field": col} for col in df.columns]
        )
    ]),
    dbc.Row([
        dcc.Input(id='input-on-submit', type='text'),
        dcc.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(
            id='container-button-basic',
            children='Enter a peptide sequence and press submit'
        )
    ])
], fluid=True)


# -------------------------
# Callback function
# -------------------------

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value) -> str:
    """
    Check if user sequence is in the dataset. If found, return peptide info.
    If not found, use saved ML model to predict primary category.
    """

    logging.info("User submitted peptide sequence")

    #Test if nothing is entered
    if value is None:
        return "Please enter a peptide sequence."

    user_sequence = value.strip().upper()
    
    #Test if empty string is entered
    if user_sequence == "":
        return "Please enter a peptide sequence."

    #Test if entered sequence matches csv
    matched_data = df[df["sequence"].astype(str).str.upper() == user_sequence]

    if len(matched_data) > 0:
        peptide_data = matched_data.iloc[0]

        return f'Your peptide is: "{peptide_data["name"]}". It is used for: "{peptide_data["primary_category"]}". FDA approved: "{peptide_data["fda_approved"]}".'

    #If sequence doesnt match call ml model
    else:
        sample_data = pd.Series([user_sequence])
        sample_features = amino_acid_features(sample_data)
        predicted_category = peptide_model.predict(sample_features)

        return f'Peptide sequence not found. This sequence is most likely used for: "{predicted_category[0]}".'

def main():
    """
    Run dashboard workflow.
    """

    logging.info("Starting dashboard")

    app.run(host='0.0.0.0', port=8050, debug=True)


if __name__ == '__main__':
    main()