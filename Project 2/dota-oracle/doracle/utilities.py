from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from tensorflow.keras.models import load_model
from tensorflow.keras import Sequential

import pandas as pd
import numpy as np
import pickle

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


def predict_hero(heroes: list, team: int = 1):
    mlp_rad = pickle.load(open('./models/model_dire.sav', 'rb'))
    mlp_dir = pickle.load(open('./models/model_radiant.sav', 'rb'))

    for j in range(4):
        bestChoice = 0
        bestWinRate = 0.
        if team == 0:
            for i in range(131, 130 * 2):
                tmp = 0
                k = 0
                for hero in heroes:
                    if i in heroes:
                        k = 0
                        break
                    tmp1 = mlp_rad.predict([[int(hero) + 130, i]])
                    tmp += float(tmp1[0])
                    k += 1

                if k == 0:
                    continue
                if tmp / k > bestWinRate:
                    bestWinRate = tmp / k
                    bestChoice = i - 130
        else:
            for i in range(1, 130):
                tmp = 0
                k = 0
                for hero in heroes:
                    if i in heroes:
                        k = 0
                        break
                    tmp1 = mlp_dir.predict([[int(hero), i]])
                    tmp += float(tmp1[0])
                    k += 1
                if k == 0:
                    continue
                if tmp / k > bestWinRate:
                    bestWinRate = tmp / k
                    bestChoice = i
        return (bestChoice, bestWinRate)


def main():
    print(predict_vs_team([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]))


if __name__ == '__main__':
    main()
