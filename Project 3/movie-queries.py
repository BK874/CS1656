# Brian Knotten
# CS 1656
# Project 2

# movie-queries.py runs the 8 specified queries and stores the query outputs in a
# file. The outputs should be stored in a single file named output.txt. Each query
# should have a header line (e.g. ### Q1 ### for the first query) followed by the
# results of the query one row at a time with commas separating multiple fields.
# If a query result is not provided a header for that query should still be
# present. Results should be ordered by query number and separated by a blank
# line as well.

# Necessary to access the database
from neo4j.v1 import GraphDatabase, basic_auth

# For connecting with authentication:
# driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j",
#                                                                   "cs1656"),
#                               encrypted=False)

# For connecting without authentication:
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)

session = driver.session()
transaction = session.begin_transaction()

# Create file and write header for first question
file = open("output.txt", "w")
file.write('### Q1 ###\n')

# Query 1: List the first 20 actors in descending order of the number of films
# they acted in.
# Output: actor_name, number_of_films_acted_in
result1 = transaction.run("""
MATCH (actor:Actor) -[:ACTS_IN]-> (movie:Movie)
RETURN actor.name AS actor_name, count(*) AS number_of_films_acted_in
ORDER BY number_of_films_acted_in DESC LIMIT 20
;""")
for record in result1:
    file.write(("%s, %s\n" %(record['actor_name'],
                             record['number_of_films_acted_in'])))

file.write('\n### Q2 ###\n')
# Query 2: List the titles of all movies with a review with at most 3 stars
# Output: movie_title
result2 = transaction.run("""
MATCH (movie:Movie) <-[rating:RATED]- (person:Person)
WHERE rating.stars <= 3
RETURN movie.title AS movie_title
;""")
for record in result2:
    file.write(("%s\n" %(record['movie_title'])))

file.write('\n### Q3 ###\n')
# Query 3: Find the movie with the largest cast, out of the list of movies that
# have a review
# Output: movie_title, number_of_cast_members
result3 =  transaction.run("""
MATCH (movie:Movie) <-[rating:RATED]- (person:Person)
WITH movie, collect(movie) AS rated
MATCH (actor:Actor) -[:ACTS_IN]-> (m:Movie)
WHERE m in rated
RETURN m.title AS movie_title, count(*) AS number_of_cast_members
ORDER BY number_of_cast_members DESC LIMIT 1
;""")
for record in result3:
    file.write(("%s, %s\n" %(record['movie_title'],
                             record['number_of_cast_members'])))

    
file.write('\n### Q4 ###\n')
# Query 4: Find all the actors who have worked with at least 3 different directors
# (regardless of how many movies they acted in). Both 3 movies with one director
# each and a single movie with 3 directors satisfy this.
# Output: actor_name, number_of_directors_he/she_has_worked_with
result4 = transaction.run("""
MATCH (actor:Actor) -[:ACTS_IN]-> (movie:Movie) <-[:DIRECTED]- (director:Director)
WITH actor, count(distinct director.name) AS number_of_directors_he_she_has_worked_with
WHERE number_of_directors_he_she_has_worked_with >= 3
RETURN distinct actor.name AS actor_name, number_of_directors_he_she_has_worked_with
;""")
for record in result4:
    file.write(("%s, %s\n" %(record['actor_name'],
                             record['number_of_directors_he_she_has_worked_with'])))

file.write('\n### Q5 ###\n')
# Query 5: List all actors whose Bacon number is exactly 2
# Output: actor_name
result5 = transaction.run("""
MATCH (bacon:Actor{name: "Kevin Bacon"}) -[:ACTS_IN]-> (movie:Movie) <-[:ACTS_IN]- (bacon1:Actor)
MATCH (bacon1:Actor)-[:ACTS_IN]->(movie2:Movie)<-[:ACTS_IN]-(bacon2:Actor)
WHERE bacon2 <> bacon AND NOT (bacon)-[:ACTS_IN]->()<-[:ACTS_IN]-(bacon2)
RETURN distinct bacon2.name AS actor_name
;""")
for record in result5:
    file.write(("%s\n" %(record['actor_name'])))

file.write('\n### Q6 ###\n')
# Query 6: List which genres have movies in which Tom Hanks stars
# Ouput: genre
result6 = transaction.run("""
MATCH(m:Movie) <-[:ACTS_IN]- (tom:Actor {name: 'Tom Hanks'}) 
RETURN distinct m.genre AS genre
;""")
for record in result6:
    file.write(("%s\n" %(record['genre'])))

file.write('\n### Q7 ###\n')
# Query 7: Show which directors have directed movies in at least 2
# different genres
# Output: director_name, number_of_genres
result7 = transaction.run("""
MATCH (director:Director) -[:DIRECTED]-> (movie:Movie)
WITH director.name AS director_name, count(distinct movie.genre) AS number_of_genres
WHERE number_of_genres >= 2
RETURN director_name, number_of_genres
;""")
for record in result7:
    file.write(("%s, %s\n" %(record['director_name'],
                             record['number_of_genres'])))

file.write('\n### Q8 ###\n')
# Query 8: Show the top 5 pairs of actor, director combinations in descending
# order of frequency of occurrence.
# Output: director_name, actor_name, number_of_times_director_directed_said_actor_in_a_movie
result8 = transaction.run("""
MATCH (director:Director) -[:DIRECTED]-> (movie:Movie) <-[:ACTS_IN]- (actor:Actor)
WITH director.name as director_name, actor.name as actor_name, count(*) as number_of_times_director_directed_said_actor_in_a_movie
RETURN distinct director_name, actor_name, number_of_times_director_directed_said_actor_in_a_movie
ORDER BY number_of_times_director_directed_said_actor_in_a_movie DESC LIMIT 5
;""")
for record in result8:
    file.write(("%s, %s, %s\n" %(record['director_name'],
                             record['actor_name'],
                             record['number_of_times_director_directed_said_actor_in_a_movie'])))

file.close()

transaction.close()
session.close()
