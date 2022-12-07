from zipfile import ZipFile
import json


class Hero:
    def __init__(self):
        self.attributes: dict = {}


def main():
    with ZipFile("./dota_games.zip", "r") as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                data = f.read()
                print(data)


if __name__ == '__main__':
    main()
