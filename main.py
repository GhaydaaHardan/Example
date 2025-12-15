from flask import Flask, request, render_template, redirect, url_for
import itertools
import math

app = Flask(__name__)

def calc_distance(p1, p2):
    return math.dist(p1, p2)


def calculate_tsp_route(locations):
    best_distance = float('inf')
    best_route = None
    start = (0, 0)
    for perm in itertools.permutations(locations):
        route = [start] + list(perm) + [start]
        total_dist = 0
        for i in range(len(route) - 1):
            total_dist += calc_distance(route[i], route[i+1])

        if total_dist < best_distance:
            best_distance = total_dist
            best_route = route

    return best_route, round(best_distance, 3)

@app.route('/')
def home():
    return render_template("home_page.html")

@app.route('/calculate', methods=['GET'])

def compute():
    try:
        raw = request.args.get("locations")
        if not raw:
            return render_template("home_page.html")
        locations = eval(raw)
        for loc in locations:
            if len(loc) != 2:
                raise ValueError
            float(loc[0]); float(loc[1])
        route, total = calculate_tsp_route(locations)
        return render_template("results.html",route=route, total=total)
    except:
        return render_template("results.html",error=True)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
