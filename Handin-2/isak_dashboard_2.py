import json
import random
import pickle
import base64

import pandas as pd
import numpy as np
import dash
from dash import dcc               
from dash import html as html
from dash.dependencies import Input, Output, State
import plotly.express as px




def parse_contents_into_auction_data(base64_content, filename):
    content_type, content_string = base64_content.split(',')
    decoded = base64.b64decode(content_string)    
    content_as_string = decoded.decode('utf-8')

    # INSERT CODE TO CONVERT TO AUCTION DATA HERE
    auction_data = content_as_string

    return content_as_string



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3(children="Isak Housing Inc - Auction Dashboard"),
    
    html.Div([
        html.H4(children="Budget (in NOK):"),
        dcc.Input(id='budget', value='0', type='number'),
    ]),

    html.Div([
        html.H4(children="Number of years:"),
        dcc.Input(id='num-years', value='1', type='number'),
    ]),

    html.Div([
        html.H4(children="Houses File:"),
        dcc.Upload(
            id='upload-data',

            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        )
    ]),
    html.H4(children="Output:"),
    html.Div([
        html.Pre(id="output-text")
    ])
])

@app.callback(Output('output-text', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('budget', 'value'),
              State('num-years', 'value'))
def run_auction(base64_content, filename, budget_raw, years_in_future_raw):

    if base64_content is None:        
        return "<empty>"

    auction_data = parse_contents_into_auction_data(base64_content, filename)
    
    budget = int(budget_raw)
    years_in_future = int(years_in_future_raw)

    houses_to_buy = "houses to buy: [ 51, 81, 12]\nEstimated earnings: 515, Years: {}, Budged: {}".format(budget, years_in_future)

    return houses_to_buy


if __name__ == '__main__':
    app.run_server(debug=True)
