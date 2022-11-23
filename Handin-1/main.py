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

    x = data[0][:, 0]  # BLUE - DEFAULT BUSY ROAD
    y = data[0][:, 1]  # BLUE - DEFAULT BUSY ROAD

    x1 = data[1][:, 0]  # PURPLE - BUSY ROAD
    y1 = data[1][:, 1]  # PURPLE - BUSY ROAD

    x2 = data[2][:, 0]  # GREEN - FERRY
    y2 = data[2][:, 1]  # GREEN - FERRY

    x3 = data[3][:, 0]  # YELLOW - FERRY
    y3 = data[3][:, 1]  # YELLOW - FERRY
    # (a, b, c, d, e, y_hat) = train(1_000_000, x2, y2)
    # regression_line = px.line(x=x, y=a * x + b)
    # result = np.polyfit(x=x, y=y, deg=3)
    # print(a, b, c, d, e)
    xs = np.linspace(500, 1200, 10000)
    plot0 = px.line(x=xs, y=272.55356191050276 + (0.0006057348957772989 * ((xs - 575.6583688060624) ** 2)) - (
                0.2839965415289085 * xs), color_discrete_sequence=['purple'])
    xs = np.linspace(500, 1200, len(x1))
    plot1 = px.line(x=xs, y=0.006014825361727816 * xs + 14.929245470922652 + 77.40763375916771,
                    color_discrete_sequence=['red'])
    # xs = np.linspace(500, 1200, 1_000)
    # plot2 = px.line(x=xs, y=87.56483941125592 + 39.95653297815632 *np.sin(((np.pi/36)*xs)-13.6)-0.05503150948226687*xs+0.00007898714277855759*xs**2, color_discrete_sequence=['green'])

    points = px.scatter(x=x, y=y)
    points1 = px.scatter(x=x1, y=y1, color_discrete_sequence=['purple'])
    points2 = px.scatter(x=x2, y=y2, color_discrete_sequence=['green'])
    points3 = px.scatter(x=x3, y=y3, color_discrete_sequence=['yellow'])

    fig = go.Figure(data=points.data + points1.data + points2.data + points3.data + plot0.data + plot1.data)
    fig.show()


if __name__ == '__main__':
    main()
