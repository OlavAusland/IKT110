import json
import plotly.express as px

def main():
    workplaces = []
    employees = {}

    workplace_data = {}
    employee_age = {}
    with open('./emp.json', 'r', encoding='utf-8') as f:
        employees = json.load(f)
    identifiers = []

    for employee in employees['employees']:
        if employee['Workplace'] not in workplaces:
            workplaces.append(employee['Workplace'])

        if employee['Age'] in employee_age:
            employee_age[employee['Age']] += 1
        else:
            employee_age[employee['Age']] = 1

    print('Workplace / Number of employees\n')
    for workplace in workplaces:
        num_employees = sum(1 for employee in employees["employees"] if employee["Workplace"] == workplace)
        print(f'{workplace} : {num_employees}')
        workplace_data[workplace] = num_employees

    print(employee_age)
    figure = px.bar(x=workplace_data.keys(), y=workplace_data.values(), text_auto=True)
    figure.show()

    age_fig = px.bar(x=employee_age.keys(), y=employee_age.values(), text_auto=True)
    age_fig.show()

    figure.write_image('./static/workplace_staff.png', scale=10)
    age_fig.write_image('./static/staff_age.png', scale=10)


if __name__ == '__main__':
    main()
