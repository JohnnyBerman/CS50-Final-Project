Webscraper

To make the website work, we first had to have a database to query on. The best place to get baseball statistics is at baseball-reference.com,
so we decided to webscrape it to get statistics for each player. After looking through their website a bit, we found that at https://www.baseball-reference.com/players/?/
where the question mark is a letter in the alphabet, there was a webpage with a list of players with last name starting with the letter where the question mark was. This list
also had each name as a link to the players statistics. We were able to webscrape the pages with question mark a-z to get the links to every player.

Once we had the link to every player, we were able to turn our attention to webscraping each players stats page and turning it into entries for each table in the database.
We decided to focus only on batting stats in the database and website searches for a couple of reasons:
1: We had a limited amount of time to complete the project, and the webscraper would have taken 36 hours instead of 12 if we included pitching stats. Since we needed to keep
watch over the webscraper to make sure that there were no issues while it ran, this would have been very difficult to do and could have compromised other aspects of our project.
2: Baseball references HTML was not very consistent, so we would have had to make significant changes to the code that would make it much more complex and tough to test, as
well as taking a lot more time.
3: The way we set up the application and database, it would be very easy to add more stats to it if we finished the basics of the project. Therefore, we wanted to invest more
time into the rest of the project to make it functioning perfectly, and then get back to adding more stats after.

Besides that, the decisions for the webscraper were fairly straightforward. We read in the data, formatted it, and saved it to the database. One issue we ran into was that
there would not be a part of the table for statistics for a player playing in a specific league or on a specific team if they only played in/on one their whole career. Because of
that, we kept track of the different teams and leagues they played in during each season, and if they only played for one took their career statistics, and made it their league/team
statistics.

Another design decision was to save the database every 100 players. Although this slowed down the program a little bit, it meant that if an error popped up due to inconsistent
HTML on baseball reference, we would not lose that much progress as each 100 players took about 30 seconds. In addition, it meant that we did not have to keep watch over the webscraper
for 12 straight hours as we could stop it in the middle, and then pick up where we left off after if we needed to.



Database

Below is our reasoning for each table in our database
Players: Giving players a player ID and using that as a foreign key in other databases perserves space and prevents confusion when there are multiple players with the same name.
career_batting_stats: Allows for people to search for what players did over their entire career easily
league_batting_stats: Allows for people to search for what players did over their entire career in a league easily
team_batting_stats: Allows for people to search for what players did over their entire career on a team easily
season_batting_stats: Allows for people to search for what players did over a season easily
teams: Allows for people to search for specific team queries
league: Allows for people to search for specific league queries



Templates

Here is the general format for our html templates:
layout.html:    This is more or less the layout template from CS50 Finance, with our javascript file included. The links in the nav bar have been updated, and the text and color scheme is diffrent.
                We used this becuase we wanted to work smarter not harder, and it makes sense to use the resources provided to us by the class as long as they fit our needs.
search.html:    This is the landing screen for StatCatch, and the starting point for a search. We have a requirement to search for either season data or multi-season data, and then each other data
                type has buttons to add or remove constraints to vary the search. We initialized zero constraints for most of the stats as they are not required for a query.
                The team/league constraint is limited to one option from a dropdown menu for now because we treat every constraint using AND logic. This is all placed in a form to submit to the next
                page via a "POST". We chose to display it this way because it is very user friendly, and does not require the user to understand the code behind what they're doing. This is a big step
                up over similar programs.
display.html:   Display is the second screen of a search, displaying the form once again in order to further narrow the search, but this time with 2 columns of checkbox elements to determine which
                stats to show in the final table. Next to this is a table of all of the players' names who fit the first search. The second form does not have to be submitted, but we wanted it to be
                possible to refine the search and display perhaps a different type of stats (season vs career) from the first search.
players.html:   This is the third and final page of the search process, with a table of players and the desired statistics. It is the only thing on this page to keep it friendly and focus the attention.
terms.html:     This page displays the meanings of various abbreviations used throughout the site for statistics, teams, and leagues. It keeps it simple and clear, just as much information as is needed.



Static

scripts.js:     This contains both the add and remove functions for the buttons, and the base html for the form elements. By adding the html, the add function makes 1 more appear. The remove function
                clears the section of constraints. The scripts were optomized to make the buttons pass in a parameter for the type of stat, making the code much more efficient.
styles.css:     This is the basic styles from CS50 Finance, but instead of aligning text center, the default has been switched to align left. In addition, extraneous nav bar text colors have been removed.
                Again, this comes down to coding smarter not harder, but we streamlined and optomized as well.



Appplication.py

There were a couple of specific design choices we had to make in here. We made reading in the query from the user a helper function, since it is the exact same in display
and in search. We returned the basic result of the query and then inside of the routes changed the results to do what we wanted them to. We made sure to have the query only add
for specific guidlines if the user added a constraint and filled it in. Otherwise the constraint was ignored. The query returned a list of dictionaries.

Inside of the display route, we knew that the only information we were getting from search was the players names that fit the query. However, if the user searched for seasons instead of
career stats, the query could return a players name multiple times if he fit the criterion in multiple seasons. Therefore, we converted it into a set of names. However, dictionaries
cannot be hashed so we changed the dictionary into just the name value, since that is all we care about in the results from search. Also, we saved this set to each session since
that is unique to each user nad could then easily be used in the players route. We could not put the result of the query in the url because if a lot of players were selected by a
query, it would be too long to fit into the url itself. If the search returned no players, we redirected them back to the search route and alerted them that their query had no results.

Inside of the players route, we started by getting the result of the query from display, made a list of stats that the user is interested in for our table, and loaded in
the saved results from the search query. Then, we converted the list of dictionaries of the name and statistics selected that came from our query to a set of tuples. We converted
it into a set to remove duplicate results as those were not wanted on the players page. However, we could not hash a dictionary for the set since dictionaries are mutable, so we
converted the values (which were always in the same order which was the order of our request in the query on the database) into a tuple which is immutable. Then, we removed all of
the results from the second query where the name of the player was not in the results from the first query. If the search returned no players, we redirected them back to the search route
and alerted them that their query had no results.



Cache

Caching would effeciently keep the n most searched queries in a dictionary where the key is the query and the value is the result. We needed a seperate dictionary to keep count
of how many times each query was made, since we wanted to keep counts for every single query. We are then able to use a couple of dictionary comprehensions and other python
built in functions to get caching to work easily. Ultimately, decided against implementing caching in the programs current state but would do so in the future. This is because
in the future, we would change the webscraper to get all of the information off of baseball reference. This would make our database at least 10 times larger, so the queries would
take a lot longer. Caching would then be useful because the most searched queries, which are likely to be searched again, will be run very quickly.