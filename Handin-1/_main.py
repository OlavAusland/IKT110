from datetime import datetime
import random

import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import tqdm
from numpy import ndarray
import pickle as pk
import numba


def load_data(filename: str) -> list:
    traffic = list()
    with open(filename, 'r') as file:
        for line in file.readlines():
            traffic.append(json.loads(line))
    return sorted(traffic, key=lambda d: d['depature'])


def to_seconds(date: datetime):
    return (date.hour * 60) + date.minute


def to_numerical(array: list) -> ndarray:
    dct: dict = {'A->C->D': 0, 'A->C->E': 1, 'B->C->D': 2, 'B->C->E': 3}
    data: np.array = [[], [], [], []]
    for elem in array:
        t0 = datetime.strptime(elem['depature'], '%H:%M')
        t1 = datetime.strptime(elem['arrival'], '%H:%M')
        data[dct[elem['road']]].append([to_seconds(t1), to_seconds(t1) - to_seconds(t0), dct[elem['road']]])

    return np.array([np.array(data[0]), np.array(data[1]), np.array(data[2]), np.array(data[3])],
                    dtype=object)


@numba.jit(nopython=True)
def get_loss(y_hat, ys):
    loss = ((y_hat - ys) ** 2).sum()
    return loss


@numba.njit()
def predict(x):
    theta = np.random.uniform(-4, 4, size=9)
    y = np.zeros_like(x)

    for i, x_k in enumerate(x):
        acc: int = 0
        for k in range(0, 9, 3):
            acc += theta[k] * np.sin(theta[k + 1] * (x_k + theta[k + 2]))
        y[i] = acc
    return y, theta


def train(iterations: int, x, y):
    best_loss = float('inf')
    best_solution = None
    for i in range(iterations):
        a = random.uniform(0, 1)
        b = random.uniform(-1, 1)
        c = random.uniform(-100, 100)
        y_hat = a * x + b
        # y_hat = (a * (x ** 2)) + (b * x) + c
        y_hat = a * x * np.sin(b * x)
        # y_hat, _ = predict(x)
        current_loss = get_loss(y_hat, y)
        if current_loss < best_loss:
            best_loss = current_loss
            best_solution = (a, b, c, y_hat)
    return best_solution


def main():
    traffic = load_data('traffic.jsonl')
    data = to_numerical(traffic)
    x = data[1][:, 0]
    y = data[1][:, 1]

    (a, b, c, y_hat) = train(100, x, y)
    # regression_line = px.line(x=x, y=a * x + b)
    result = np.polyfit(x=np.arange(x, ), y=y, deg=3)
    polynomial = px.line(x=x, y=y_hat)
    points = px.scatter(x=x, y=y)

    fig = go.Figure(data=points.data + polynomial.data)
    fig.show()


if __name__ == '__main__':
    main()
