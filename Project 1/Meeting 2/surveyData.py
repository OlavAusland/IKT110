import csv
import numpy as np


def printSortedDictionary(employeesData):
    for i in sorted(employeesData):
        print(i, round(eval(employeesData[i]) / ((len(employeesData[i]) + 1) / 2),1))
    print('\n')
    return


def main():
    workplaces = {}
    age = {}
    with open('./survey.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Where do you work?'] in workplaces:
                workplaces[f"{row['Where do you work?']}"] = workplaces[row['Where do you work?']] + '+' + row[
                    'From 1-10, how happy are you working at SEBS CAFE?']
            else:
                workplaces[f"{row['Where do you work?']}"] = row['From 1-10, how happy are you working at SEBS CAFE?']

            if row['How old are you?'] in age:
                age[f"{row['How old are you?']}"] = age[row['How old are you?']] + '+' + row[
                    'From 1-10, how happy are you working at SEBS CAFE?']
            else:
                age[f"{row['How old are you?']}"] = row['From 1-10, how happy are you working at SEBS CAFE?']

    printSortedDictionary(workplaces)
    printSortedDictionary(age)


if __name__ == '__main__':
    main()
