import json
import plotly.express as px
import requests


def read_data():
    with open('emp.json', 'r') as file:
        emp_data = json.load(file)
        return emp_data['employees']


def get_population(city):
    api_url = f'https://api.api-ninjas.com/v1/city?name={city}'
    response = requests.get(api_url, headers={'X-Api-Key': 'cW6jX4siIIMBhaMY2EF0WA==UqhzsmmuNa9CjsaQ'})
    data = response.json()
    return int(data[0]['population'])


def main():
    emp_data = read_data()

    workplace_data = {}

    for employee in emp_data:
        if employee['Workplace'] in workplace_data:
            workplace_data[employee['Workplace']] += 1
        else:
            workplace_data[employee['Workplace']] = 1

    fig = px.bar(x=workplace_data.keys(), y=workplace_data.values(), text_auto=True)
    fig.write_image('./static/workplace_employees_ratio.png', scale=10)


if __name__ == '__main__':
    main()
