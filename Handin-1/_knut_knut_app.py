import random
from flask import Flask
from flask import request
import datetime
import pickle as pk

app = Flask(__name__)


def estimate_route(route: int) -> int:
    model = pk.load(f'./models/model_{route}.csv')


def get_the_best_route_as_a_text_informatic(dep_hour, dep_min):
    roads = ["A->C->D", "A->C->E", "B->C->D", "B->C->E"]

    # perform some magic here - instead of just a random selection
    est_travel_time = random.randint(10, 120)
    best_road = random.choice(roads)

    out = """
    <p>
    Departure time: {}:{} <br> 
    Best travel route: {} <br> 
    Estimated travel time of {} minutes. </p> 
    <p><a href="/">Back</a></p>
    """.format(dep_hour, dep_min, best_road, est_travel_time)

    return out


@app.route('/')
def get_departure_time():
    return """
    <h3>Knut Knut Transport AS</h3>
        <form action="/get_best_route" method="get">
            <label for="hour">Hour:</label>
            <select name="hour" id="hour">
                <option value="06">06</option>
                <option value="07">07</option>
                <option value="08">08</option>
                <option value="09">09</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>
                <option value="13">13</option>
                <option value="14">14</option>
                <option value="15">15</option>
                <option value="16">16</option>     
            </select>
            
            <label for="mins">Mins:</label>
            <input type="text" name="mins" size="2"/>
            <input type="submit">
        </form>
    """


@app.route("/get_best_route")
def get_route():
    departure_h = request.args.get('hour')
    departure_m = request.args.get('mins')

    route_info = get_the_best_route_as_a_text_informatic(departure_h, departure_m)
    return route_info


if __name__ == '__main__':
    print("<starting>")
    app.run()
    print("<done>")

