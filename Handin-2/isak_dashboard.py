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
from main import House, predict_house_value, load_model, load_data
from typing import List
import tqdm


def parse_contents_into_auction_data(base64_content, filename):
    content_type, content_string = base64_content.split(',')
    decoded = base64.b64decode(content_string)
    content_as_string = decoded.decode('utf-8')

    # INSERT CODE TO CONVERT TO AUCTION DATA HERE
    dict_list = [d.strip() for d in content_as_string.splitlines()]

    houses: List[House] = []
    for d in dict_list:
        houses.append(House(data=json.loads(d)))

    return houses

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

    houses: List[House] = []
    houses = load_data(houses, 'train.jsonl')

    # sort
    auction_data = sorted(auction_data, key=lambda x: x.data['auction_price'])
    for i, house in enumerate(auction_data):
        if house.data['auction_price'] > budget:
            auction_data = auction_data[0:i]
            break

    if len(auction_data) <= 0:
        return "No prediction for budget, please increase poor bitch"
    else:
        print(f'Houses Left: {len(auction_data)}')
    # implemented knapsack

    profitable = []
    houses_to_buy = []

    for house in tqdm.tqdm(auction_data):
        predicted = predict_house_value(house, houses=houses, delta_year=years_in_future, model='./new_model.csv')
        house.data['predicted'] = predicted
        diff = predicted - house.data['auction_price']
        if 0 < diff < 2000000:
            house.data['profit'] = diff
            profitable.append(house)

    profitable = sorted(profitable, key=lambda x: x.data['profit'], reverse=True)
    count = 0

    for house in profitable:
        if count + house.data['auction_price'] < budget:
            houses_to_buy.append(house)
            count += house.data['auction_price']

    if years_in_future == 0:
        return ":c"
    return "\nEstimated earnings: {:,}\nHouses to buy: {}".format(sum(house.data['profit'] for house in houses_to_buy),
                                                                  houses_to_buy)


if __name__ == '__main__':
    app.run_server(debug=True)
