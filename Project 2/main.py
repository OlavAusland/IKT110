from zipfile import ZipFile
import json
from tqdm import tqdm
from typing import List
import numpy as np
import operator
import math
import numba
import csv


class Hero:
    def __init__(self):
        self.attributes: dict = {}


class GameResult:
    def __init__(self, player_features: list = ['hero_id']):
        self.player_features = player_features
        self.data = {'players': {'dire': [], 'radiant': []},
                     'radiant_win': False,
                     'game_mode': 22,
                     'duration': -1}


def extract_data():
    """
    Extract the most important data from the dota dataset and save to a custom json file.
    :return:
    """
    wanted_features = ['players', 'radiant_win', 'game_mode', 'duration']

    games: List[GameResult] = []
    with ZipFile("./dota_games.zip", "r") as z:
        for filename in tqdm(z.namelist()):
            with z.open(filename) as f:
                try:
                    game_result: GameResult = GameResult()
                    data = json.loads(f.read())['result']
                    if data['game_mode'] == 22:
                        for feature in wanted_features:
                            if feature == 'players':
                                for i in range(0, len(data[feature])):
                                    for player_feature in game_result.player_features:
                                        game_result.data[feature]['dire' if i >= 5 else 'radiant'].append(data[feature][i][player_feature])
                            else:
                                game_result.data[feature] = data[feature]
                        if 0 not in game_result.data['players']['dire'] and 0 not in game_result.data['players']['radiant']:
                            games.append(game_result)
                except Exception as error:
                    print(f'Failed: {error}')
    with open('./data.json', 'w') as file:
        data = json.dumps([obj.data for obj in games])
        file.write(data)


def load_data(file: str = './data.json'):
    with open(file, 'r') as file:
        return json.loads(file.read())


def get_most_played_hero(data: dict):
    """
    Get the most frequently played hero by id.
    :param data: Data to search for most frequently played hero.
    :return: Most frequently played hero id.
    """
    heroes_frequency = {}

    for game in data:
        for player in game['players']['dire']:
            if player in heroes_frequency.keys():
                heroes_frequency[player] += 1
            else:
                heroes_frequency[player] = 1
        for player in game['players']['radiant']:
            if player in heroes_frequency.keys():
                heroes_frequency[player] += 1
            else:
                heroes_frequency[player] = 1

    result = max(heroes_frequency, key=heroes_frequency.get, default=None)
    return result


def get_highest_win_rate_hero(data: dict):
    heroes = {}

    for game in data:
        for player in game['players']['dire']:
            if player in heroes.keys():
                heroes[player]['losses' if bool(game['radiant_win']) else 'wins'] += 1
            else:
                heroes[player] = {'wins': 0, 'losses': 0}
        for player in game['players']['radiant']:
            if player in heroes.keys():
                heroes[player]['wins' if bool(game['radiant_win']) else 'losses'] += 1
            else:
                heroes[player] = {'wins': 0, 'losses': 0}
    win_percentage = {}
    print(heroes)
    for (key, value) in heroes.items():
        win_percentage[key] = float(value['wins'] / (value['wins'] + value['losses']))
    result = max(win_percentage, key=win_percentage.get, default=None)

    with open("./data/win_rate.json", "w") as outfile:
        json.dump(win_percentage, outfile)

    return {result: win_percentage[result]}


def get_longest_shortest_game_pair(data: dict):
    heroes = {}
    for game in data:
        for (team_key, team_value) in game['players'].items():
            for player in team_value:
                if player in heroes.keys():
                    heroes[player]['total_time'] = heroes[player]['total_time'] + game['duration']
                    heroes[player]['games'] = heroes[player]['games'] + 1
                    heroes[player]['average_time'] = (heroes[player]['total_time'] / heroes[player]['games'])
                else:
                    heroes[player] = {'total_time': 0, 'games': 0}

    highest = {'hero': -1, 'time': -math.inf}
    lowest = {'hero': -1, 'time': math.inf}
    for (key, value) in heroes.items():
        if value['average_time'] > highest['time']:
            highest = {'hero': key, 'time': value['average_time']}
        if value['average_time'] < lowest['time']:
            lowest = {'hero': key, 'time': value['average_time']}
    return lowest, highest


def get_team_win_rate(data: dict):
    team_wins = {'dire': 0, 'radiant': 0}

    for game in data:
        team_wins['radiant' if game['radiant_win'] else 'dire'] += 1
    return {'dire_win_percentage': team_wins['dire'] / (team_wins['dire'] + team_wins['radiant']),
            'radiant_win_percentage': team_wins['radiant'] / (team_wins['dire'] + team_wins['radiant'])}


def get_most_affected_hero_by_side(data: dict):
    result = {'dire': {}, 'radiant': {}}

    for game in data:
        for i, team in enumerate(game['players']):
            for player in team:
                winner = 'radiant' if game['radiant_win'] else 'dire'

    return result


def get_heroes() -> list:
    with open('./heroes.json', 'rb') as file:
        return json.loads(file.read())


def data_cleanup(data: str = './data.json'):
    with open(data, 'w+') as file:
        data = json.loads(file.read())

        for i, game in enumerate(data):
            if 0 in game['players']['radiant'] or 0 in game['players']['dire']:
                del data[i]

        file.write(data)


def get_pick_rate(data: dict):
    result: dict = {}

    for game in data:
        for (team_key, team_value) in game['players'].items():
            for player in team_value:
                if player in result.keys():
                    result[int(player)]['rounds'] += 1
                else:
                    result[int(player)] = {'rounds': 1}
    for (key, value) in result.items():
        result[key]['pick_rate'] = (value['rounds'] / len(data))

    with open("./data/pick_rate.json", "w") as outfile:
        json.dump(result, outfile)
    return result


def get_best_pair(file: str = './data/pair_win_rate.csv'):
    result = {} # {'pair_id': 0, 'win_rate': 0}

    with open(file, 'r') as file:
        data = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        next(data)

        for row in data:
            if int(row[0]) in result.keys():
                if result[int(row[0])]['win_rate'] < float(row[2]):
                    result[int(row[0])]['pair_id'] = int(row[1])
                    result[int(row[0])]['win_rate'] = float(row[2])
            else:
                result[int(row[0])] = {'pair_id': int(row[1]), 'win_rate': float(row[2])}

    with open('./data/best_duo.json', 'w') as file:
        json.dump(result, file)

    return result


def main():
    data: dict = json.loads(open('./data.json').read())
    # get_pick_rate(data)
    # get_highest_win_rate_hero(data)
    get_best_pair()
    # extract_dat()
    # data_cleanup()
    """
    data = load_data()
    print(f'1. {get_most_played_hero(data)}')
    print(f'2. {get_highest_win_rate_hero(data)}')
    print(f'3. {get_team_win_rate(data)}')
    print(f'\ta. Unknown')
    print(f'4. Unknown')
    print(f'5-6. {get_longest_shortest_game_pair(data)}')
    print(f'7. Unknown')
    print(f'8. Unknown')
    print(f'9. Unknown')
    print(get_heroes())
    """


if __name__ == '__main__':
    main()
