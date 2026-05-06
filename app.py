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
    df = pd.read_csv('model/peptide_list_expanded.csv')

    with open('model/peptide_category_pipeline.pkl', 'rb') as f:
        peptide_model = pickle.load(f)

except FileNotFoundError:
    logging.error("File not found. Exiting.")
    sys.exit(1)


# -------------------------
# Dashboard values
# -------------------------

total_peptides = len(df)
total_categories = df["primary_category"].nunique()
avg_length = round(df["length"].mean(), 1)

if "fda_approved" in df.columns:
    fda_count = len(df[df["fda_approved"].astype(str).str.lower().isin(["yes", "true", "1"])])
else:
    fda_count = 0

category_fig = px.histogram(
    df,
    x="primary_category",
    title="Primary Category Distribution"
)

category_fig.update_layout(
    template="plotly_white",
    height=360,
    margin=dict(l=30, r=30, t=60, b=120),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Arial", size=12),
    title=dict(font=dict(size=20))
)

category_fig.update_xaxes(title="", tickangle=35)
category_fig.update_yaxes(title="Peptide Count")


# -------------------------
# Dash app
# -------------------------

external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Container([

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("PEPTIDE INTELLIGENCE PLATFORM", style={
                        "fontSize": "13px",
                        "fontWeight": "700",
                        "letterSpacing": "2.5px",
                        "color": "#7dd3fc",
                        "marginBottom": "18px"
                    }),

                    html.H1("Peptide Sequence Reader", style={
                        "fontSize": "62px",
                        "fontWeight": "800",
                        "letterSpacing": "-2px",
                        "color": "white",
                        "marginBottom": "18px"
                    }),

                    html.P(
                        "Search curated peptide records, review biological metadata, "
                        "and classify unknown sequences with a trained machine learning model.",
                        style={
                            "fontSize": "20px",
                            "color": "#cbd5e1",
                            "maxWidth": "850px",
                            "margin": "0 auto 34px auto",
                            "lineHeight": "1.6"
                        }
                    ),

                    html.Div([
                        dcc.Input(
                            id='input-on-submit',
                            type='text',
                            placeholder='Enter peptide sequence...',
                            style={
                                "width": "72%",
                                "height": "58px",
                                "paddingLeft": "20px",
                                "paddingRight": "20px",
                                "fontSize": "18px",
                                "borderRadius": "14px",
                                "border": "none",
                                "backgroundColor": "#ffffff",
                                "color": "#111827",
                                "outline": "none",
                                "boxShadow": "0 10px 30px rgba(0,0,0,0.18)"
                                }
                        ),

                        dcc.Button(
                            'Analyze',
                            id='submit-val',
                            n_clicks=0,
                            style={
                                "padding": "16px 30px",
                                "fontSize": "17px",
                                "fontWeight": "700",
                                "borderRadius": "14px",
                                "border": "none",
                                "background": "linear-gradient(135deg, #38bdf8, #2563eb)",
                                "color": "white",
                                "marginLeft": "12px",
                                "boxShadow": "0 10px 25px rgba(37,99,235,0.35)",
                                "cursor": "pointer"
                            }
                        )
                    ], style={"textAlign": "center"}),

                    html.Div(
                        id='container-button-basic',
                        children='Enter a peptide sequence and press analyze.',
                        style={
                            "margin": "28px auto 0 auto",
                            "padding": "18px 22px",
                            "maxWidth": "850px",
                            "fontSize": "18px",
                            "backgroundColor": "rgba(255,255,255,0.10)",
                            "border": "1px solid rgba(255,255,255,0.18)",
                            "borderRadius": "18px",
                            "color": "#e2e8f0",
                            "backdropFilter": "blur(10px)"
                        }
                    )
                ], style={
                    "padding": "70px 35px",
                    "textAlign": "center",
                    "background": "radial-gradient(circle at top left, #2563eb 0%, #0f172a 42%, #020617 100%)",
                    "borderRadius": "30px",
                    "boxShadow": "0 25px 70px rgba(15,23,42,0.28)",
                    "marginTop": "34px",
                    "marginBottom": "30px"
                })
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Total Peptides", style={"color": "#64748b", "fontSize": "14px", "fontWeight": "700"}),
                    html.Div(f"{total_peptides}", style={"fontSize": "34px", "fontWeight": "800", "color": "#0f172a"})
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "22px",
                    "padding": "24px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0"
                })
            ], md=3),

            dbc.Col([
                html.Div([
                    html.Div("Categories", style={"color": "#64748b", "fontSize": "14px", "fontWeight": "700"}),
                    html.Div(f"{total_categories}", style={"fontSize": "34px", "fontWeight": "800", "color": "#0f172a"})
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "22px",
                    "padding": "24px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0"
                })
            ], md=3),

            dbc.Col([
                html.Div([
                    html.Div("FDA Approved", style={"color": "#64748b", "fontSize": "14px", "fontWeight": "700"}),
                    html.Div(f"{fda_count}", style={"fontSize": "34px", "fontWeight": "800", "color": "#0f172a"})
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "22px",
                    "padding": "24px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0"
                })
            ], md=3),

            dbc.Col([
                html.Div([
                    html.Div("Avg. Length", style={"color": "#64748b", "fontSize": "14px", "fontWeight": "700"}),
                    html.Div(f"{avg_length}", style={"fontSize": "34px", "fontWeight": "800", "color": "#0f172a"})
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "22px",
                    "padding": "24px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0"
                })
            ], md=3)
        ], className="g-4 mb-4"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Category Landscape", style={
                        "fontSize": "26px",
                        "fontWeight": "800",
                        "color": "#0f172a",
                        "marginBottom": "4px"
                    }),
                    html.Div(
                        "Overview of peptide functional categories represented in the dataset.",
                        style={
                            "fontSize": "15px",
                            "color": "#64748b",
                            "marginBottom": "18px"
                        }
                    ),
                    dcc.Graph(figure=category_fig, config={"displayModeBar": False})
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "24px",
                    "padding": "28px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0",
                    "marginBottom": "30px"
                })
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div("Peptide Dataset", style={
                        "fontSize": "28px",
                        "fontWeight": "800",
                        "color": "#0f172a",
                        "marginBottom": "4px"
                    }),

                    html.Div(
                        "Curated peptide records used for lookup and model prediction.",
                        style={
                            "fontSize": "15px",
                            "color": "#64748b",
                            "marginBottom": "22px"
                        }
                    ),

                    dag.AgGrid(
                        rowData=df.to_dict('records'),
                        columnDefs=[{"field": col} for col in df.columns],
                        defaultColDef={
                            "sortable": True,
                            "filter": True,
                            "resizable": True
                        },
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 10
                        },
                        style={
                            "height": "520px",
                            "width": "100%"
                        },
                        className="ag-theme-quartz"
                    )
                ], style={
                    "backgroundColor": "white",
                    "borderRadius": "26px",
                    "padding": "30px",
                    "boxShadow": "0 14px 35px rgba(15,23,42,0.08)",
                    "border": "1px solid #e2e8f0",
                    "marginBottom": "50px"
                })
            ])
        ])

    ], fluid=True, style={
        "paddingLeft": "45px",
        "paddingRight": "45px"
    })
], style={
    "backgroundColor": "#f8fafc",
    "minHeight": "100vh",
    "fontFamily": "Arial, sans-serif"
})


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

    if value is None:
        return "Please enter a peptide sequence."

    user_sequence = value.strip().upper()

    if user_sequence == "":
        return "Please enter a peptide sequence."

    matched_data = df[df["sequence"].astype(str).str.upper() == user_sequence]

    if len(matched_data) > 0:
        peptide_data = matched_data.iloc[0]

        return html.Div([
            html.Div("Sequence Found", style={
                "fontSize": "15px",
                "fontWeight": "800",
                "letterSpacing": "1.5px",
                "color": "#86efac",
                "marginBottom": "8px"
            }),
            html.Div(f'Your peptide is: "{peptide_data["name"]}".', style={
                "fontSize": "20px",
                "fontWeight": "700",
                "color": "white",
                "marginBottom": "6px"
            }),
            html.Div(f'It is used for: "{peptide_data["primary_category"]}".', style={
                "fontSize": "17px",
                "color": "#e2e8f0",
                "marginBottom": "4px"
            }),
            html.Div(f'FDA approved: "{peptide_data["fda_approved"]}".', style={
                "fontSize": "17px",
                "color": "#e2e8f0"
            })
        ])

    else:
        sample_data = pd.Series([user_sequence])
        sample_features = amino_acid_features(sample_data)
        predicted_category = peptide_model.predict(sample_features)

        return html.Div([
            html.Div("Sequence Not Found", style={
                "fontSize": "15px",
                "fontWeight": "800",
                "letterSpacing": "1.5px",
                "color": "#fde68a",
                "marginBottom": "8px"
            }),
            html.Div("The entered sequence was not found in the peptide dataset.", style={
                "fontSize": "17px",
                "color": "#e2e8f0",
                "marginBottom": "6px"
            }),
            html.Div(f'This sequence is most likely used for: "{predicted_category[0]}".', style={
                "fontSize": "20px",
                "fontWeight": "700",
                "color": "white"
            })
        ])


def main():
    """
    Run dashboard workflow.
    """

    logging.info("Starting dashboard")

    app.run(host='0.0.0.0', port=8050, debug=True)


if __name__ == '__main__':
    main()