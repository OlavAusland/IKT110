import csv
import time
import numpy as np
import itertools
import re
import pandas as pd


def createDuoData(data, duoWrite):
    duoData = np.full((130, 130, 3), 0)

    team_value_map = {
        'Dire': 1,
        'Radiant': 0
    }

    # open the input file for reading
    with open(data, 'r') as input_file:
        reader = csv.reader(input_file)
        next(reader)

        for row in reader:
            gameData = np.full(12, 0)
            count = 0

            for value, field in enumerate(row):
                # skip irrelevant fields
                if (value % 2 == 0) and (value <= 20):
                    continue
                if field.isdigit():
                    gameData[count] = field
                else:
                    gameData[count] = team_value_map.get(field, 0)
                count += 1

            # skips the game if game time is zero
            if gameData[11] == 0:
                continue

            # create the team arrays for both teams
            teamRadiant = np.sort(gameData[:5])
            teamDire = np.sort(gameData[5:10])

            # create the combinations arrays for both teams
            combinationsRadiant = np.unique(list(itertools.combinations(teamRadiant, 2)), axis=0)
            combinationsDire = np.unique(list(itertools.combinations(teamDire, 2)), axis=0)

            # determine which team won the game
            winning_team = 'Dire' if gameData[11] > 0 else 'Radiant'

            # iterate over the combinations of both teams
            for team, combinations in (('Dire', combinationsDire), ('Radiant', combinationsRadiant)):
                # iterate over the combinations for the current team
                for duo in combinations:
                    if duo[0] == duo[1]:
                        print("here", duo[0])
                    # update the win/loss count for the current duo
                    duoData[duo[0]][duo[1]][0 if team == winning_team else 1] += 1

                    # update the score for the current duo
                    duoData[duo[0]][duo[1]][2] += gameData[11]

    with open(duoWrite, 'w', newline='', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerows(duoData)

    return


def duoWinRate(data, winRateWrite):
    duoData = np.full((130, 130), 0.)
    with open(data, 'r') as input_file:
        reader = csv.reader(input_file)
        for row, r in enumerate(reader):
            for colum, field in enumerate(r):
                numbers = re.findall(r'\d+', field)
                if numbers[0] == '0' and numbers[1] == '0':
                    continue
                duoData[row][colum] = float((100. / (float(numbers[0]) + float(numbers[1]))) * float(numbers[0]))

    with open(winRateWrite, 'w', newline='', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(duoData)
    return


def teamWinRate(data, winRateWrite):
    with open(winRateWrite, 'w', newline='', encoding='UTF8') as f:
        f.writelines("1, 2, 3, 4, 5, Win Rate\n")
        with open(data, 'r') as input_file:
            reader = csv.reader(input_file)
            next(reader)
            for row, r in enumerate(reader):
                rowString = ""
                numbers = 0.
                number = 0.
                for colum, field in enumerate(r):
                    if colum < 5:
                        rowString += field + ","
                        continue
                    numbers += float(field)
                    if number == 0:
                        number = float(field)
                rowString += str(round((100. / numbers) * number, 2)) + "\n"
                f.writelines(rowString)

    return


def findHighestWinRateDuo(winRateDuo):
    amountOfCombinations = 10
    with open(winRateDuo, 'r') as input_file:
        reader = csv.reader(input_file)
        highest = np.full((3, amountOfCombinations), 0.)
        for row, r in enumerate(reader):
            for colum, field in enumerate(r):
                for i in range(amountOfCombinations):
                    if float(field) > highest[0][i]:
                        highest[0][i] = float(field)
                        highest[1][i] = row + 1  # +1 because of the header
                        highest[2][i] = colum + 1  # +1 because of the header
                        break
    for i in range(amountOfCombinations):
        print("Highest win rate duos: ", int(highest[1][i]), "and", int(highest[2][i]), "\t:", round(highest[0][i], 2),
              "%")
    return


def sortedCSV(data, write):
    team_value_map = {
        'Dire': 1,
        'Radiant': 0
    }
    with open(data, newline='') as input_file:
        reader = csv.reader(input_file)

        # open the output file and create a writer
        with open(write, 'w', newline='') as output_file:
            writer = csv.writer(output_file)

            # read the header row from the input file and write it to the output file
            next(reader)

            for row in reader:
                gameData = np.full(13, 0)
                count = 0

                for value, field in enumerate(row):
                    # skip irrelevant fields
                    if (value % 2 == 0) and (value <= 20):
                        continue
                    if field.isdigit():
                        gameData[count] = field
                    else:
                        gameData[count] = team_value_map.get(field, 0)
                    count += 1

                # skips the game if game time is zero
                if gameData[11] == 0:
                    continue

                # create the team arrays for both teams
                teamRadiant = np.sort(gameData[:5])
                teamDire = np.sort(gameData[5:10])

                writer.writerow((teamRadiant[0], teamRadiant[1], teamRadiant[2], teamRadiant[3], teamRadiant[4],
                                 teamDire[0], teamDire[1], teamDire[2], teamDire[3], teamDire[4], gameData[10],
                                 gameData[11]))
    return


def winRateHero(data):
    heroWinRate = np.full((130, 3), 0.)
    with open(data, newline='') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            for i in range(5):
                heroWinRate[int(row[i])][0] += 1
                heroWinRate[int(row[i])][1] += 1 if row[10] == '0' else 0
            for i in range(5, 10):
                heroWinRate[int(row[i])][0] += 1
                heroWinRate[int(row[i])][2] += 1 if row[10] == '1' else 0
    for i in range(130):
        if heroWinRate[i][0] == 0:
            continue
        heroWinRate[i][0] = (100. / heroWinRate[i][0]) * (heroWinRate[i][1] + heroWinRate[i][2])
        # print(i, heroWinRate[i][0])
    #  sort the array by win rate and keep track of the hero id
    # Get the indices that would sort the heroWinRate array in ascending order by the win rate
    sortedByWinRate = np.argsort(heroWinRate[:, 0])
    # print()
    # Print the sorted heroWinRate array and the corresponding hero IDs
    for i in sortedByWinRate:
        if i == 0 or round(heroWinRate[i][0]) == 0:
            continue
        print("Highest win rate hero: ", i, ":", round(heroWinRate[i][0], 2), "%")

    return


def createTeamData(data, write):
    gameCombination = {}
    df = pd.read_csv(data, header=None)
    df = df.values

    combination1 = df[:, :5]
    combination2 = df[:, 5:10]
    result = df[:, 10]

    for i in range(len(combination1)):
        var = 1 if result[i] == 0 else 0
        if tuple(combination1[i]) in gameCombination:
            gameCombination[tuple(combination1[i])][var] = gameCombination[tuple(combination1[i])][var] + 1
        else:
            gameCombination.setdefault(tuple(combination1[i]), [0, 0])
            gameCombination[tuple(combination1[i])][var] = 1
    for i in range(len(combination2)):
        var = 1 if result[i] == 1 else 0
        if tuple(combination2[i]) in gameCombination:
            gameCombination[tuple(combination1[i])][var] = gameCombination[tuple(combination1[i])][var] + 1
        else:
            gameCombination.setdefault(tuple(combination1[i]), [0, 0])
            gameCombination[tuple(combination1[i])][var] = 1

    with open(write, 'w') as f:
        f.writelines("1, 2, 3, 4, 5, Win, Defeat\n")
        for key, value in gameCombination.items():
            f.writelines(f"{key[0]}, {key[1]}, {key[2]}, {key[3]}, {key[4]}, {value[0]}, {value[1]}\n")

    return


def heroGameTime(data, write):
    heroAvgGameTime = np.full((130, 2), 0.)
    with open(data, newline='') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            for i in range(5):
                heroAvgGameTime[int(row[i])][0] += 1
                heroAvgGameTime[int(row[i])][1] += float(row[11])
            for i in range(5, 10):
                heroAvgGameTime[int(row[i])][0] += 1
                heroAvgGameTime[int(row[i])][1] += float(row[11])
    for i in range(130):
        if heroAvgGameTime[i][0] == 0:
            continue
        heroAvgGameTime[i][1] = heroAvgGameTime[i][1] / heroAvgGameTime[i][0]
    #  sort the array by win rate and keep track of the hero id
    # Get the indices that would sort the heroWinRate array in ascending order by the win rate
    sortedByAvgGameTime = np.argsort(heroAvgGameTime[:, 1])

    # Create an empty csv file
    with open(write, 'w') as f:
        f.writelines("Hero, Avg time\n")
    # Print the sorted heroWinRate array and the corresponding hero IDs
    for i in sortedByAvgGameTime:
        if i == 0 or round(heroAvgGameTime[i][1]) == 0:
            continue
        # store in a csv file
        with open(write, 'a') as f:
            f.writelines(f"{i}, {round(heroAvgGameTime[i][1])}\n")
        # print("Highest avg game time hero: ", i, ":", round(heroAvgGameTime[i][1], 2), "s")

    return


def findHighestWintRatedDependingOnTeam(data, write):
    # Load the data set into a DataFrame
    df = pd.read_csv(data, header=None)
    df = df.values

    teamRadiant = df[:, :5]
    teamDire = df[:, 5:10]
    result = df[:, 10]

    # Create an empty csv file
    with open(write, 'w') as f:
        f.writelines("Hero, Radiant, Win rate, Dire, Win rate\n")

    # Create a dictionary to store the win rate of each hero in the radiant team
    radiantWinRate = {}
    # Create a dictionary to store the win rate of each hero in the dire team
    direWinRate = {}

    # Loop through the radiant team
    for i in range(len(teamRadiant)):
        # Loop through the heroes in the radiant team
        for j in range(len(teamRadiant[i])):
            # If the hero is already in the dictionary
            if teamRadiant[i][j] in radiantWinRate:
                # Add 1 to the number of games played
                radiantWinRate[teamRadiant[i][j]][0] += 1
                # If the radiant team won, add 1 to the number of wins
                if result[i] == 0:
                    radiantWinRate[teamRadiant[i][j]][1] += 1
            # If the hero is not in the dictionary, add it
            else:
                radiantWinRate.setdefault(teamRadiant[i][j], [1, 0])
                # If the radiant team won, add 1 to the number of wins
                if result[i] == 0:
                    radiantWinRate[teamRadiant[i][j]][1] += 1
    # Loop through the dire team
    for i in range(len(teamDire)):
        # Loop through the heroes in the dire team
        for j in range(len(teamDire[i])):
            # If the hero is already in the dictionary
            if teamDire[i][j] in direWinRate:
                # Add 1 to the number of games played
                direWinRate[teamDire[i][j]][0] += 1
                # If the dire team won, add 1 to the number of wins
                if result[i] == 1:
                    direWinRate[teamDire[i][j]][1] += 1
            # If the hero is not in the dictionary, add it
            else:
                direWinRate.setdefault(teamDire[i][j], [1, 0])
                # If the dire team won, add 1 to the number of wins
                if result[i] == 1:
                    direWinRate[teamDire[i][j]][1] += 1

    # write the data to a csv file
    for (radiant_key, radiant_value), (dire_key, dire_value) in zip(radiantWinRate.items(), direWinRate.items()):
        # print(radiant_key, radiant_value, dire_key, dire_value)
        # return
        with open(write, 'a') as f:
            f.writelines(f"{radiant_key}, {radiant_value[0]}, {round(radiant_value[1] / radiant_value[0], 2)}, {dire_value[0]}, {round(dire_value[1] / dire_value[0], 2)}\n")

    return

def heroThatTeamHaveTheMostToSayForWinRate(data):
    # Load the data set into a DataFrame
    df = pd.read_csv(data)
    df = df.values

    highestDiff = np.full(10, 0.)
    highestDiffHero = np.full(10, 0)

    for row in df:
        radiantWinRate = 0.
        for i, field in enumerate(row):
            if i % 2 == 0 and i > 0 and radiantWinRate == 0:
                radiantWinRate = float(field)
            elif i % 2 == 0 and i > 0 and radiantWinRate != 0:
                for j in range(highestDiff.size):
                    if radiantWinRate - float(field) > highestDiff[j]:
                        highestDiff[j] = radiantWinRate - float(field)
                        highestDiffHero[j] = row[0]
                        break

    for i in range(highestDiff.size):
        print("Hero:", highestDiffHero[i], "diff in win rate according to team: ", round(highestDiff[i], 2))



if __name__ == '__main__':
    st = time.time()
    csvGameData = "combinedDataGameMode22.csv"
    csvSortedGameData = "sortedDataGameMode22.csv"

    csvDuoData = "duoData.csv"
    csvTeamData = "teamData.csv"

    csvDuoWinRate = "winRateDuo.csv"
    csvTeamWinRate = "winRateTeam.csv"
    csvHeroGameTime = "heroGameTime.csv"
    csvTeamWinRateDependingOnTeam = "teamWinRateDependingOnTeam.csv"

    # createDuoData(csvGameData, csvDuoData)
    # duoWinRate(csvDuoData, csvDuoWinRate)
    # findHighestWinRateDuo(csvDuoWinRate)
    # sortedCSV(csvGameData, csvSortedGameData)
    # winRateHero(csvSortedGameData)
    # createTeamData(csvSortedGameData, csvTeamData)
    # teamWinRate(csvTeamData, csvTeamWinRate)
    # heroGameTime(csvSortedGameData, csvHeroGameTime)
    # findHighestWintRatedDependingOnTeam(csvSortedGameData, csvTeamWinRateDependingOnTeam)
    heroThatTeamHaveTheMostToSayForWinRate(csvTeamWinRateDependingOnTeam)
    print(time.time() - st)
