Welcome to our website! Here, you can use simple english commands to find out the answer complex baseball batting statistics questions you may have.
To begin, go into terminal and into the final directory. Then, type in flask run, hit enter, and go to the link provided.

To use our website, you will be directed to the search page. Here, you can add different constraints to search for players. For example, if you choose
the options
Stat Type: Individual Seasons
Season Constraints: Player's (n)th season—1
Stat Constraints: HR > 25
You will search for all players who hit more than 25 home runs in their first year playing. Then, you will be directed to the display page. Here, you can
see a list of all players who fit the criterion you put into the search page, and another set of criterion to input. Here, you can search for specific things
about the players selected in the search page. For example, if you choose the options
Stat Type: Multi_Season Totals
Stat Constraints: HR > 200
Stats to Display: HR, RBI
You will be sent to players.html and see the career totals of HR and RBI for all the players selected in the first page who hit at least 200 home runs in their career.


There are 4 main components to the code of the project, all listed below

CS50 Webscraper is the ipython notebook we used to webscrape all of the players batting statistics on baseball reference and save it to a sql database.

player_data.db is the database that stores the tables containing the data that our website uses. Inside of it is
career_batting_stats: The batting stats for an entire players career
league_batting_stats: The batting stats for the entire time a player played in a certain league
team_batting_stats: The batting stats for the entire time a player played on a certain team
season_batting_stats: The batting stats for each year a player played
league: All of the leagues a player played for
teams: All of the teams a player played for
players: All of the players unique player ID's used throughout the database

Inside of the static and template folders are where our javascript, css, and html are held for our website. Script.js is the code that is
run whenever a constraint is supposed to be added or removed as indicated by button clicks.

Application.py is where our flask code is held for our website. Inside of there, we have the routes for two of our webpages, search.html which searches
which is the initial search for specific players that fit the criterion requested and display.html which shows the players found and has a form to choose which
specific things the user wants to search for that player (it could be nothing or something more complicated like career home runs as long as they had 500 hits
in their career).
The method get_players() processes the commands given on search.html and display.html and returns the sql query slightly formatted.


In addition to the above code, we have a caching feature that keeps the N most common searches on the server in CS50 cache that is not yet implemented. This is because
the data base is relatively small (our project focused purely on simple batting statistics while there are over 100 statistics per player on baseball-reference) so the
queries do not take too long. However, once more data is added and queries start taking longer we would implement this to save time fo the user.