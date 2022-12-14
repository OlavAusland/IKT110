from tensorflow.keras.models import load_model
from tensorflow.keras import Sequential
import numpy as np


def champs_to_input(dire: list = (1, 2, 3, 4, 5), radiant: list = (6, 7, 8, 9, 10)):
    encoded = np.zeros(shape=(272,))

    for player in dire:
        encoded[player] = 1
    for player in radiant:
        encoded[player + 136] = 1

    return encoded


def predict_vs_team(dire: np.array, radiant: np.array) -> list:
    """
    Function to predict win-rate based on full teams.
    :rtype: list
    :return: [x, y] - x = percentage of dire win, y = percentage of radiant win
    """
    model: Sequential = load_model('./models/default.h5')
    data = champs_to_input(dire=dire, radiant=radiant)
    prediction = model.predict(np.array([data]))

    return prediction


def main():
    print(predict_vs_team([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]))


if __name__ == '__main__':
    main()
