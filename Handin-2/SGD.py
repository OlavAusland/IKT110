import numpy as np
import plotly.express as px
import numba
from typing import Tuple, Union
import tqdm

@numba.njit()
def predict(theta, xs):
    return np.dot(xs, theta)


def J_squared_residual(theta, xs, y):
    h = predict(theta, xs)
    sr = ((h - y)**2).sum()
    return sr


def gradient_J_squared_residual(theta, xs, y):
    h = predict(theta, xs)
    grad = np.dot(xs.transpose(), (h - y))
    return grad


def get_subset(xs: np.array, ys: np.array, indexes: np.array, batch_size: int) -> Union[Tuple[np.array, np.array], Tuple[None, None]]:
    if (len(xs) < batch_size) or (len(xs) != len(ys)) or (len(indexes) < batch_size):
        return None, None

    x_data = np.empty([batch_size, len(xs[0])])
    y_data = np.empty([batch_size, 1])

    np.random.shuffle(indexes)

    for i in range(0, batch_size):
        x_data[i] = xs[indexes[i]]
        y_data[i] = ys[indexes[i]]

    return x_data, y_data


def train(xs: np.ndarray, ys: np.ndarray, learning_rate: float,
          iters: int, batch_percentage: float, summary: bool = False) -> Union[np.ndarray, None]:
    """
    :param xs: X data
    :param ys: Y data
    :param learning_rate: Learning rate
    :param iters: Number of iterations to improve on
    :param batch_percentage: Stochastic batch size
    :param summary: Print information about the training data
    :return: thetas / weight
    """

    n_features = xs.shape[1]
    theta = np.zeros((n_features, 1))
    m = xs.shape[0]

    # run SGD
    j_history = []

    for it in tqdm.tqdm(range(iters)):
        x, y = get_subset(xs, ys, np.arange(0, len(xs)), int(len(xs) * batch_percentage))

        if x is None:
            print("Bad Input In 'get_subset()'")
            return None
        j = J_squared_residual(theta, x, y)
        j_history.append(j)

        theta = theta - (learning_rate * (1 / m) * gradient_J_squared_residual(theta, x, y))

    j = J_squared_residual(theta, xs, ys)
    j_history.append(j)

    y_pred = predict(theta, xs)
    l1_error = np.abs(y_pred - ys).sum()

    u = ((ys - y_pred) ** 2).sum()
    v = ((ys - ys.mean()) ** 2).sum()

    if summary:
        print(f"Thetas: {theta}")
        print("The L2 error is: {:.2f}".format(j))
        print("The L1 error is: {:.2f}".format(l1_error))
        print("R^2: {:.2f}".format(1 - (u / v)))

        fig = px.scatter(j_history, title="J(theta) - Loss History")
        fig.show()

    return theta
