import csv

male = []
female = []
with open('Meeting 1/survey.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(', '.join(row))

        if row['Gender'] == "Male":
            male.append(row['From 1-10, how happy are you working at SEBS CAFE?'])
        else:
            female.append(row['From 1-10, how happy are you working at SEBS CAFE?'])

female = [eval(i) for i in female]
male = [eval(i) for i in male]
print("Male score:", sum(male) / (len(male) - 1))
print("Female score:", sum(female) / (len(female) - 1))
