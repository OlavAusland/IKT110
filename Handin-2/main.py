import json
import csv
import random
from typing import List, Union, Optional, Type
from numpy import genfromtxt

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import numba
import tqdm
from SGD import train
import datetime


class House:
    def __init__(self, data: dict):
        self.data: dict = {}
        for (key, value) in data.items():
            self.data[key] = value

        self.features: list

    def update_values(self, data: dict):
        for (key, value) in data.items():
            self.data[key] = value

    def __repr__(self):
        output = f"House: {self.data['id']}\n"

        for (key, value) in self.data.items():
            if key == 'id':
                continue
            if key == 'color':
                output += f"{str(key).upper()}: {value}\n"
                continue
            if key in ['price', 'auction_price']:
                output += '{}: {:,}\n'.format(str(key).upper(), value)
                continue
            output += f"{str(key).upper()}: {value}\n"

        output += "-" * 50
        output += '\n'
        return output


def erase_all(keywords: list, string: str) -> str:
    string = str(string)
    for keyword in keywords:
        string = string.replace(keyword, "")

    return eval(string)


def parse_line(line: dict) -> Union[dict, None]:
    # colors = ["gray", "red", "white", "black", "green"]
    colors = {"gray": 3, "red": 4, "white": 2, "black": 1, "green": 5, "undefined": 0}

    for (key, value) in line.items():
        if key == 'price':
            if "mil" in str(line["price"]):
                line["price"] = int(float(line["price"].replace("mil", "")) * 10e5)
            line["price"] = line["price"] = erase_all([" "], line["price"])
        if key == 'color':
            if line["color"] not in colors.keys():
                line["color"] = "undefined"
            line['color'] = colors[line['color']]
        if key == 'built':
            if len(str(line['built'])) == 2:
                line['built'] = eval("19" + str(line['built']))

    return line


def load_data(houses: List[House], file_path: str):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            curr_house = parse_line(json.loads(line))
            if any(house.data['id'] == curr_house['id'] for house in houses):
                for house in houses:
                    if house.data['id'] == curr_house['id']:
                        house.update_values(curr_house)
            else:
                houses.append(House(curr_house))
    return houses


def plot(xs, ys, show=False, color='cyan', x_label: str = 'X - Axis', y_label: str = 'Y - Axis'):
    scatter = px.scatter(x=xs, y=ys, color_discrete_sequence=[color])
    figure = go.Figure(data=scatter.data)
    figure.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    if show:
        figure.show()

    return scatter


def get_normalized_features(houses: List[House], wanted_features: list) -> np.ndarray:
    if len(houses) <= 0:
        return None
    min_values, max_values = {}, {}

    for key in wanted_features:
        min_values[key] = (min(houses, key=lambda x: x.data[key]).data[key])
        max_values[key] = (max(houses, key=lambda x: x.data[key]).data[key])

    normalized_values: List[List] = []

    for house in houses:
        features = []

        for key in wanted_features:
            features.append((house.data[key] - min_values[key]) / (max_values[key] - min_values[key]))

        normalized_values.append(features)

    return np.array([np.array(x) for x in normalized_values])


def get_features(houses: List[House], wanted_features: list) -> Union[np.ndarray, None]:
    if len(houses) <= 0:
        return None

    values: List[List] = []
    for house in houses:
        features = []

        for key in wanted_features:
            features.append(house.data[key])
        values.append(features)
    return np.array([np.array(x) for x in values])


def remove_outliers(houses: List[House], bot_perc, top_perc):
    temp = sorted(houses, key=lambda x: x.data['price'])
    temp = temp[int(len(houses) * (bot_perc / 2)):]
    temp = temp[:len(temp) - int(len(houses) * (top_perc / 2))]
    return temp


def denormalize(value: float, houses: List[House], feature: str) -> int:
    minimum = (min(houses, key=lambda x: x.data[feature]).data[feature])
    maximum = (max(houses, key=lambda x: x.data[feature]).data[feature])

    return value * (maximum - minimum) + minimum


def normalize_feature(value: float, houses: List[House], feature: str) -> float:
    minimum = (min(houses, key=lambda x: x.data[feature]).data[feature])
    maximum = (max(houses, key=lambda x: x.data[feature]).data[feature])

    return (value - minimum) / (maximum - minimum)


def normalize(value: float, minimum, maximum) -> float:
    return (value - minimum) / (maximum - minimum)


def preprocess_data(houses: List[House]):
    houses = remove_outliers(houses, 0.1, 0.1)
    return houses


def normalized_to_profit(p1, p2, houses: List[House]) -> int:
    p2 = denormalize(p2, houses, 'price')

    return p2 - p1


def load_model(model: str = './model.csv'):
    with open(model, 'r') as f:
        data = list(csv.reader(f, delimiter=","))

    data = np.array(data, dtype=float)

    theta = data[0]
    minimum = data[1]
    maximum = data[2]

    return theta, minimum, maximum


def predict_house_value(house: House, houses: List[House], delta_year: int = 0, model: str = './model.csv'):
    time = datetime.date.today()
    theta, minimum, maximum = load_model(model)
    year = time.year

    if 'year' in house.data.keys():
        year = house.data['year']

    predicted_price = (normalize_feature(house.data['size'], houses, 'size') * theta[0] +
                       normalize_feature(house.data['built'], houses, 'built') * theta[1] +
                       normalize_feature(house.data['sun'], houses, 'sun') * theta[2] +
                       normalize_feature(year + delta_year, houses, 'year') * theta[3])

    return denormalize(predicted_price, houses, 'price')


def knapsack(houses: List[House], budget: int):
    result: List[House] = []

    if len(houses) == 0:
        return


def main():
    """
    houses: List[House] = load_data('train.jsonl')

    houses = preprocess_data(houses)
    # theta = train(get_normalized_features(houses, ['size', 'sun', 'built', 'year']),
    #              get_normalized_features(houses, ['price']), 0.02, 10000, 0.3, summary=False)
    theta = load_model()
    print(predict_house_value(houses[0], delta_year=3))
    print(houses[0].data['price'])
    print(houses[0])

    norm = get_normalized_features(houses, ['size', 'sun', 'built', 'year'])
    index = 2000

    price = houses[index].data['price']
        #(norm[index][0] * theta[0] +
         #    norm[index][1] * theta[1] +
          #   norm[index][2] * theta[2] +
           #  norm[index][3] * theta[3])

    predicted_price = (norm[index][0] * theta[0] +
                       norm[index][1] * theta[1] +
                       norm[index][2] * theta[2] +
                       normalize_feature(denormalize(norm[index][3], houses, 'year')+3, houses, 'year') * theta[3])
    print(houses[index].data['price'])
    print(denormalize(predicted_price, houses, 'price'))
    print(normalized_to_profit(price, predicted_price, houses), end='\n\n')
    predict_house_value(houses[0])
    """


    # houses: List[House] = []
    # houses = load_data(houses, 'train.jsonl')
    # houses = remove_outliers(houses, 0, 0))

    # sorted_houses = sorted(houses, key=lambda x: x.data['price'])
    # print(sorted_houses[0], sorted_houses[-1])

    houses: List[House] = []
    houses = load_data(houses, 'train.jsonl')

    index = random.randint(0, len(houses) - 1)
    price = predict_house_value(houses[index], houses, 0, './new_model.csv')
    print('predicted: {:,}, actual: {:,}, diff: {:,}'.format(price, houses[index].data["price"], price - houses[index].data["price"]))

    max_error = 0

    for house in houses:
        price = predict_house_value(house, houses, 0, './new_model.csv')

        max_error = abs(price - house.data["price"])
        print('Predicted: {:,}\nActual: {:,}\nAbs Diff: {:,}'.format(price, house.data['price'], abs(price - house.data["price"])), end='\n\n')
        print(house)

    print(max_error)


if __name__ == '__main__':
    main()
