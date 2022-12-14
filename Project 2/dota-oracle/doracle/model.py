import random
import json


class HeroStats:
    def __init__(self):
        self.pick_rate = -1
        self.win_rate = -1
        self.best_paired = -1

    def get_winrate(self, hero_id):
        with open('./data/win_rate.json') as file:
            data = json.loads(file.read())

            if str(hero_id) in data.keys():
                self.win_rate = data[str(hero_id)]
                return f'{round(self.win_rate * 100, 2)}%'
        return -1
    def get_pickrate(self, hero_id):
        with open('./data/pick_rate.json') as file:
            data = json.loads(file.read())

            if str(hero_id) in data.keys():
                self.pick_rate = data[str(hero_id)]['pick_rate']
                return f'{round(self.pick_rate * 100, 2)}%'
        return -1

    def get_best_paired_with_hero(self, hero_id):
        with open('./data/best_duo.json') as file:
            data = json.loads(file.read())

            if str(hero_id) in data.keys():
                self.best_paired = data[str(hero_id)]['pair_id']
                return self.best_paired
        return -1

    @staticmethod
    def load(path_to_model: str):
        print("loading model from: {}".format(path_to_model))
        return HeroStats()
