import json
from typing import List


class Employee:
    def __init__(self, data: dict):
        self.id = data['Id']
        self.workplace = data['Workplace']
        self.salary = data['Salary NOK']
        self.age = data['Age']
        self.yac = data['YAC']

        self.data = data

    def __repr__(self):
        output: str = '\n' + '-' * 50 + '\n'

        for (key, value) in self.data.items():
            output += f'{str(key).upper()} -> {value}\n'

        output += '-' * 50 + '\n'
        return output


def load_data(file: str = './combinedEmp.json') -> List[Employee]:
    with open(file, 'r') as file:
        result: List[Employee] = []
        data = json.load(file)

        for employee in data['employees']:
            result.append(Employee(data=employee))
        return result


def main():
    employees = load_data()
    data = {'workplace_avg_salary': {}}

    for employee in employees:
        if employee.workplace in data['workplace_avg_salary']:
            data['workplace_avg_salary'][employee.workplace] += (employee.salary / len(employees))
        elif employee.workplace not in data['workplace_avg_salary']:
            data['workplace_avg_salary'][employee.workplace] = (employee.salary / len(employees))

    print(data)


if __name__ == '__main__':
    main()
