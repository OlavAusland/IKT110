import random
from flask import Flask
from flask import request

app = Flask(__name__)


def get_the_best_route_as_a_text_informatic(dep_hour, dep_min):
    roads = ["A->C->D", "A->C->E", "B->C->D", "B->C->E"]
    dep_hour = int(dep_hour)
    if dep_min.isdigit():
        dep_min = int(dep_min)
    else:
        dep_min = 0
    # perform some magic here - instead of just a random selection
    if (dep_hour * 60 + dep_min) < 626 or (dep_hour * 60 + dep_min) > 1003:
        est_travel_time = 0.006014825361727816 * (dep_hour * 60 + dep_min) + 14.929245470922652 + 77.40763375916771
        best_road = roads[1]
    else:
        est_travel_time = 272.55356191050276 + (
                0.0006057348957772989 * (((dep_hour * 60 + dep_min) - 575.6583688060624) ** 2)) - (
                                  0.2839965415289085 * (dep_hour * 60 + dep_min))
        best_road = roads[0]

    out = """
    <p>
    Departure time: {}:{} <br> 
    Best travel route: {} <br> 
    Estimated travel time of {} minutes. </p> 
    <p><a href="/">Back</a></p>
    """.format(dep_hour, dep_min, best_road, int(est_travel_time))

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
