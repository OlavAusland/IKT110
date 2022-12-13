import random


class HeroStats:
    def __init__(self):
        pass

    def get_winrate(self, hero_id):
        return random.random()

    def get_pickrate(self, hero_id):
        return random.random()

    def get_best_paired_with_hero(self, hero_id):
        return random.randint(0, 120)

    @staticmethod
    def load(path_to_model: str):
        print("loading model from: {}".format(path_to_model))
        return HeroStats()
