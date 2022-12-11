import json
import zipfile
import csv
import re
import time


def createEmptyCsvWhiteHeader(csvFile):
    header = ['Game', 'Hero 0', 'Team', 'Hero 1', 'Team', 'Hero 2', 'Team', 'Hero 3', 'Team', 'Hero 4', 'Team',
              'Hero 5',
              'Team', 'Hero 6', 'Team', 'Hero 7', 'Team', 'Hero 8', 'Team', 'Hero 9', 'Team', 'Winner', 'Duration']
    with open(csvFile, 'w') as csv_file:
        dw = csv.DictWriter(csv_file, delimiter=',', fieldnames=header)
        dw.writeheader()


def main(csvFile, zipFile):
    data = None
    gameCounter = 0

    with zipfile.ZipFile(zipFile, "r") as z:
        for file in z.namelist():
            # print(file)
            findChamp = 0
            playerCounter = 0
            with z.open(file) as f:
                data = f.read().decode('utf-8')
                if data.find("game_mode\":22") > 0:
                    dataLines = data.splitlines()
                    wl = [gameCounter]
                    gameCounter += 1
                    for rl in dataLines:
                        if rl.find("player_slot") > 0:
                            findChamp = 1
                            continue

                        if findChamp == 1 and playerCounter <= 4:
                            # if re.findall(r'\d+', rl)[0] == '0':
                            #     print(file)
                            #     print(data)
                            findChamp = 0
                            playerCounter += 1
                            wl.append(re.findall(r'\d+', rl)[0])
                            wl.append("Radiant")
                        elif findChamp == 1:
                            # if re.findall(r'\d+', rl)[0] == '0':
                            #     print(file)
                            #     print(data)
                            findChamp = 0
                            playerCounter += 1
                            wl.append(re.findall(r'\d+', rl)[0])
                            wl.append("Dire")
                        elif playerCounter <= 9:
                            continue
                        elif rl.find("radiant_win\":false") > 0:
                            wl.append("Dire")
                        elif rl.find("radiant_win\":true") > 0:
                            wl.append("Radiant")
                        elif rl.find("duration") > 0:
                            wl.append(re.findall(r'\d+', rl)[0])
                            break
                    if wl:
                        with open(csvFile, 'a', newline='', encoding='UTF8') as csv_file:
                            writer_object = csv.writer(csv_file)
                            writer_object.writerow(wl)


def gameModes(zipFile):
    game = {}

    with zipfile.ZipFile(zipFile, "r") as z:
        for file in z.namelist():
            with z.open(file) as f:
                data = f.read().decode('utf-8')
                dataLines = data.splitlines()
                for rl in dataLines:
                    if rl.find("game_mode") > 0:
                        if game.get(f"{rl}") is not None:
                            game[rl] = (1 + int(game[rl]))
                        else:
                            game[rl] = 1

    print(game)


if __name__ == '__main__':
    st = time.time()
    csvPath = "test.csv"
    zipPath = "./dota_games.zip"
    createEmptyCsvWhiteHeader(csvPath)
    main(csvPath, zipPath)
    # gameModes(zipPath)
    print(time.time() - st)
