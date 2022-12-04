import json


def main():
    employees = []
    employees1 = {}
    employees2 = {}

    employees.append('employees : [')

    with open('./../Meeting 1/emp.json', 'r', encoding='utf-8') as f:
        employees1 = json.load(f)

    with open('./emp.json', 'r', encoding='utf-8') as f:
        employees2 = json.load(f)

    for employee in employees1['employees']:
        combinedEmployee = str(employee)
        for __employee in employees2['employees']:
            if __employee["Id"] == employee['Id']:
                combinedEmployee += ', \'YAC\': \'' + str(__employee['YAC']) + '\', \'Salary NOK\': \'' + str(__employee['Salary NOK']) + '\''
                combinedEmployee = combinedEmployee.translate({ord(c): None for c in "}"})
                combinedEmployee = combinedEmployee.replace('\\t', '') + '},'
                break
        employees.append(combinedEmployee)

    employees.append(']')
    json_object = json.dumps(employees, indent=6)
    print(json_object)
    with open("combinedEmp.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    main()
