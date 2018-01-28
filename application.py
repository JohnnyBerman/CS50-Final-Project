from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///player_data.db")

@app.route("/")
def search():
    return render_template("search.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/display", methods=["GET", "POST"])
def display():
    if request.method == "POST":
        try:
            # Finds all the players that fit the first search and save the result
            players = get_players()
            players = {list(ele.values())[0] for ele in players}

            session["result"] = players # https://stackoverflow.com/questions/27611216/how-to-pass-a-variable-between-flask-pages

            if len(players) == 0:
                print("E404: No Players Found")
                flash("E404: No Players Found")
                return redirect("/") # There were no players we should do somequery

            print(players)
            return render_template("display.html", players=players)
        except:
            print("Somequery went WRONG")
            flash("We struck out on that one. Try a different request?")
            return redirect("/") #Somequery went wrong
    else:
        return render_template("display.html")


@app.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "POST":
        try:
            players = get_players()
            result = {i for i in session["result"]}
            stats = list(players[0].keys())
            stats = [i.replace("_", " ") for i in stats]

            """ Format the players and statistics into a set of tuples from a list of dictionaries to remove duplicates.
            A dictionary of dictionaries not used since dictionaries are mutable so they cannot be hashed """
            players = {tuple(ele.values()) for ele in players}

            # Get all of the players and statistics that fit both pages criterion
            players = {ele if ele[0] in result else None for ele in players}

            # Remove all the players that fit the first criterion but not the second one
            if None in players:
                players.remove(None)

            # No players fit the request
            if len(players) == 0:
                print("E404: No Players Found")
                flash("E404: No Players Found")
                return redirect("/") # There were no players we should do somequery

            return render_template("players.html", players=players, stats=stats)
        except:
            print("Stats no go")
            flash("We weren't able to display that for some reason. Sorry!")
            return redirect("/") #Somequery went wrong
    else:
        return render_template("players.html")

def get_players(players = None):
    # range is "total" or "season"
    range = request.form.get("range")

    # seasons is the array of constraints
    seasons = request.form.getlist("seasons") # https://stackoverflow.com/questions/24808660/sending-a-form-array-to-flask

    # seaNum is the array of numbers, corresponds to the constraints
    seaNum = request.form.getlist("seaNum")

    # stats is the array of stat constraints
    stats = request.form.getlist("stat")

    # stat_constraint is the array of "equal" "greater" or "less"
    stat_constraint = request.form.getlist("statconstraint")

    # stat_num is the array of numbers corresponds to stat and statconstraint
    stat_num = request.form.getlist("statNum")

    # name is "includes" "first" "last" "starts" "ends"
    name = request.form.getlist("name")

    # name_text is an array of Strings that corresponds with name
    name_text = request.form.getlist("nameConst")

    # pos_type is (array of) "include" or "exclude"
    pos_type = request.form.getlist("posType")

    # pos is (array of) the positions to include or exclude
    pos = request.form.getlist("pos")

    # pos_type is (array of) "include" or "exclude"
    team_type = request.form.get("teamType")

    # pos is (array of) the positions to include or exclude
    team = request.form.get("team")

    statbox = request.form.getlist("statbox")

    statbox.insert(0, "Name")
    columns = ", ".join(statbox)

    # Choose the correct table based on what the user entered
    tables = []
    if range == "season":
        tables.append("season_batting_stats")
    elif range == "career":
        if team == "AL" or team == "NL" or team == "AA" or team == "NA" or team == "UA" or team == "PL":
            tables.append("league_batting_stats")
        elif team != "0":
            tables.append("team_batting_stats")
        else:
            tables.append("career_batting_stats")

    query = "SELECT " + columns + " FROM players JOIN "
    query += " JOIN ".join([i + " ON " + i + ".ID = players.ID" for i in tables])

    started = False
    # Add information about individual seasons if it requested
    if all([len(i) != 0 for i in seaNum]) and len(seaNum) != 0:
        started = True
        query += " WHERE "
        query += " AND ".join(" ".join(["Year" if season_type[0] == "x" else "Season", ">" if season_type[1:6] == "after" else "<" if season_type[1:7] == "before" else "=", num]) for season_type, num in zip(seasons, seaNum))

    # Add information about individual stats if it requested
    if all([len(i) != 0 for i in stat_num]) and len(stat_num) != 0:
        if started:
            query += " AND "
        else:
            query += " WHERE "
        query += " AND ".join([" ".join([a, b, c]) for a, b, c in zip(stats, stat_constraint, stat_num)])
        started = True

    # https://www.w3schools.com/sql/sql_like.asp
    # Add information about individual names if it requested
    for n, nt in zip(name, name_text):
        if started:
            query += " AND "
        else:
            query += " WHERE "
        query += "Name LIKE "
        query += "'%" if n == "includes" else "'"
        query += nt + "%'"
        started = True

    # https://www.w3schools.com/sql/sql_like.asp
    # Add information about individual positions if it requested
    for t, p in zip(pos_type, pos):
        prefix = "LIKE" if t == "include" else "NOT LIKE"
        if started:
            query += " AND "
        else:
            query += " WHERE "
        if p == "0":
            query += "(Position " + prefix + " '%" + "1" + "%'"
            query += " OR Position " + prefix + " '%" + "2" + "%'"
            query += " OR Position " + prefix + " '%" + "3" + "%'"
            query += " OR Position " + prefix + " '%" + "4" + "%'"
            query += " OR Position " + prefix + " '%" + "5" + "%'"
            query += " OR Position " + prefix + " '%" + "6" + "%'"
            query += " OR Position " + prefix + " '%" + "7" + "%'"
            query += " OR Position " + prefix + " '%" + "8" + "%'"
            query += " OR Position " + prefix + " '%" + "9" + "%')"
        elif p == "if":
            query += "(Position " + prefix + " '%" + "3" + "%'"
            query += " OR Position " + prefix + " '%" + "4" + "%'"
            query += " OR Position " + prefix + " '%" + "5" + "%'"
            query += " OR Position " + prefix + " '%" + "6" + "%')"
        elif p == "of":
            query += "(Position " + prefix + " '%" + "7" + "%'"
            query += " OR Position " + prefix + " '%" + "8" + "%'"
            query += " OR Position " + prefix + " '%" + "9" + "%')"
        else:
            query += "Position " + prefix + " '%" + p + "%'"
        started = True

    # Add information about individual teams if it requested
    if team != "0":
        if started:
            query += " AND "
        else:
            query += " WHERE "
        query += "League" if team == "AL" or team == "NL" or team == "AA" or team == "NA" or team == "UA" or team == "PL" else "Team"
        query += " = " if team_type == "include" else " != "
        query += "'" + team + "'"

    return db.execute(query)