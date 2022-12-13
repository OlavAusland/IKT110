from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, Sequential
from tensorflow.keras.models import load_model
import numpy as np
import json
import tqdm

INPUT_SHAPE = (136 * 2,)
OUTPUT_SHAPE = 2

EPOCH_SIZE = 100
BATCH_SIZE = 10


def create_model() -> Sequential:
    """
    Create our sequential model.
    :return:
    """
    model = Sequential(
        [
            layers.Input(shape=INPUT_SHAPE),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(OUTPUT_SHAPE, activation='softmax')
        ]
    )

    model.summary()
    model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def load_data(file: str = './data.json'):
    x_train, y_train = [], []

    with open(file, 'r') as file:
        data = json.loads(file.read())
        for game in tqdm.tqdm(data):
            encoded = np.zeros(shape=(INPUT_SHAPE[0],))

            for player in game['players']['dire']:
                encoded[player] = 1
            for player in game['players']['radiant']:
                encoded[player + 136] = 1
            x_train.append(encoded)
            y_train.append([int(1 - int(game['radiant_win'])), int(game['radiant_win'])])
    x_train, x_test, y_train, y_test = train_test_split(np.asarray(x_train), np.asarray(y_train),
                                                        train_size=0.8, random_state=42)
    return x_train, x_test, y_train, y_test


def champs_to_input(dire: list = (1, 2, 3, 4, 5), radiant: list = (6, 7, 8, 9, 10)):
    encoded = np.zeros(shape=(INPUT_SHAPE[0],))

    for player in dire:
        encoded[player] = 1
    for player in radiant:
        encoded[player + 136] = 1

    return encoded


def train():
    x_train, x_test, y_train, y_test = load_data()
    model = create_model()
    model.fit(x_train, y_train, epochs=EPOCH_SIZE, batch_size=BATCH_SIZE, validation_data=(x_test, y_test))
    model.save('./models/default.h5')
    print(model.evaluate(x_test, y_test, batch_size=BATCH_SIZE))


def predict(model_path: str = './models/default.h5', dire=[18, 39, 29, 101, 14], radiant=[84, 56, 70, 40, 104]):
    model: Sequential = load_model(model_path)

    data = champs_to_input(dire, radiant)

    prediction = model.predict(np.array([data]))

    print(prediction)


def main():
    # train()

    non_champion_id = [24, 115, 116, 117, 118, 122, 123, 124, 125, 127]
    enemies = [36, 27, 41, 31, 98]
    champion_pool = np.arange(1, 130)

    champion_pool = list(set(champion_pool) - set(non_champion_id) - set(enemies))

    print(champion_pool)

    predict(dire=np.random.choice(champion_pool, 5), radiant=enemies)


if __name__ == '__main__':
    main()
