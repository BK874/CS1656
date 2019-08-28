# Brian Knotten
# CS1656
# Project 4

import sqlite3 as lite
import csv
import re
con = lite.connect('cs1656.sqlite')

with con:
        cur = con.cursor()
        ########################################################################                
        ### CREATE TABLES ######################################################
        ########################################################################                
        # DO NOT MODIFY - START 
        cur.execute('DROP TABLE IF EXISTS Actors')
        cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

        cur.execute('DROP TABLE IF EXISTS Movies')
        cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

        cur.execute('DROP TABLE IF EXISTS Directors')
        cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

        cur.execute('DROP TABLE IF EXISTS Cast')
        cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

        cur.execute('DROP TABLE IF EXISTS Movie_Director')
        cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
        # DO NOT MODIFY - END

        ########################################################################                
        ### READ DATA FROM FILES ###############################################
        ########################################################################                
        # actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
        # UPDATE THIS
        with open('actors.csv', 'r') as inputFile:
                inReader = csv.reader(inputFile, delimiter = ',',
                                      quotechar = '|')
                for row in inReader:
                        cur.execute("INSERT INTO Actors VALUES("+row[0]+", '"+
                                    row[1]+"', '"+row[2]+"', '"+row[3]+"')")
        with open('cast.csv', 'r') as inputFile:
                inReader = csv.reader(inputFile, delimiter = ',',
                                      quotechar = '|')
                for row in inReader:
                        cur.execute("INSERT INTO Cast VALUES("+row[0]+", "+
                                    row[1]+", '"+row[2]+"')")
        with open('directors.csv', 'r') as inputFile:
                inReader = csv.reader(inputFile, delimiter = ',',
                                      quotechar = '|')
                for row in inReader:
                        cur.execute("INSERT INTO Directors VALUES("+row[0]+", '"+
                                    row[1]+"', '"+row[2]+"')")
        with open('movie_dir.csv', 'r') as inputFile:
                inReader = csv.reader(inputFile, delimiter = ',',
                                      quotechar = '|')
                for row in inReader:
                        cur.execute("INSERT INTO Movie_Director VALUES("+row[0]+", "+
                                    row[1]+")")
        with open('movies.csv', 'r') as inputFile:
                inReader = csv.reader(inputFile, delimiter = ',',
                                      quotechar = '|')
                for row in inReader:
                        cur.execute("INSERT INTO Movies VALUES("+row[0]+", '"+
                                    row[1]+"', "+row[2]+", "+row[3]+")")
                        





        ########################################################################                
        ### INSERT DATA INTO DATABASE ##########################################
        ########################################################################                
        # UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
        cur.execute("INSERT OR IGNORE INTO Actors VALUES(1001, 'Harrison', 'Ford', 'Male')") 
        cur.execute("INSERT OR IGNORE INTO Actors VALUES(1002, 'Daisy', 'Ridley', 'Female')")   

        cur.execute("INSERT OR IGNORE INTO Movies VALUES(101, 'Star Wars VII: The Force Awakens', 2015, 8.2)") 
        cur.execute("INSERT OR IGNORE INTO Movies VALUES(102, 'Rogue One: A Star Wars Story', 2016, 8.0)")
        
        cur.execute("INSERT OR IGNORE INTO Cast VALUES(1001, 101, 'Han Solo')")  
        cur.execute("INSERT OR IGNORE INTO Cast VALUES(1002, 101, 'Rey')")  

        cur.execute("INSERT OR IGNORE INTO Directors VALUES(5000, 'J.J.', 'Abrams')")  
        
        cur.execute("INSERT OR IGNORE INTO Movie_Director VALUES(5000, 101)")  

        con.commit()
        
        

        ########################################################################                
        ### QUERY SECTION ######################################################
        ########################################################################                
        queries = {}

        # DO NOT MODIFY - START         
        # DEBUG: all_movies ########################
        queries['all_movies'] = '''
SELECT * FROM Movies
'''     
        # DEBUG: all_actors ########################
        queries['all_actors'] = '''
SELECT * FROM Actors
'''     
        # DEBUG: all_cast ########################
        queries['all_cast'] = '''
SELECT * FROM Cast
'''     
        # DEBUG: all_directors ########################
        queries['all_directors'] = '''
SELECT * FROM Directors
'''     
        # DEBUG: all_movie_dir ########################
        queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''     
        # DO NOT MODIFY - END

        ########################################################################                
        ### INSERT YOUR QUERIES HERE ###########################################
        ########################################################################                
        # NOTE: You are allowed to also include other queries here (e.g., 
        # for creating views), that will be executed in alphabetical order.
        # We will grade your program based on the output files q01.csv, 
        # q02.csv, ..., q12.csv

        # Q01 ########################          
        queries['q01'] = '''
        SELECT Actors.fname, Actors.lname
        FROM Actors
        INNER JOIN Cast c1 on c1.aid = actors.aid
        INNER JOIN Cast c2 on c2.aid = actors.aid
        INNER JOIN Movies m1 on m1.mid = c1.mid
        INNER JOIN Movies m2 on m2.mid = c2.mid
        WHERE m1.year >= 1990 AND m1.year <= 1999 AND m2.year > 2009
        GROUP BY lname
        ORDER BY lname, fname ASC
        '''     
        
        # Q02 ########################          
        queries['q02'] = '''
        SELECT Movies.title, Movies.year
        FROM Movies
        INNER JOIN Movies m1 ON m1.title = "Star Wars VII: The Force Awakens"
        WHERE m1.year = Movies.year AND Movies.rank > m1.rank
        ORDER BY Movies.title ASC
        '''     

        # Q03 ########################          
        queries['q03'] = '''
        SELECT DISTINCT Actors.fname, Actors.lname, COUNT(DISTINCT m1.mid)
        FROM Actors
        INNER JOIN Cast c1 on c1.aid = Actors.aid 
        INNER JOIN Movies m1 on c1.mid = m1.mid
        WHERE m1.title LIKE "%Star Wars%"
        GROUP BY lname
        ORDER BY COUNT(DISTINCT m1.mid) DESC
        '''     

        # Q04 ########################
        cur.execute("DROP VIEW IF EXISTS b41987")
        cur.execute("CREATE VIEW b41987 AS SELECT a1.fname AS first, a1.lname AS last, a1.aid as aid, m1.year AS year FROM Actors a1, Movies m1, Cast c1 WHERE m1.mid = c1.mid AND a1.aid = c1.aid;")
        queries['q04'] = '''
        SELECT b1.first, b1.last, b1.year
        FROM b41987 b1
        INNER JOIN (SELECT aid, MAX(year) AS old FROM b41987 GROUP BY aid) b2 ON b1.aid = b2.aid AND b1.year = b2.old
        WHERE b1.year < 1987
        ORDER BY last, first ASC
        '''     

        # Q05 ########################          
        queries['q05'] = '''
        SELECT d.fname, d.lname, COUNT(*) AS cnt
        FROM Movie_Director as md
        INNER JOIN Directors d ON d.did = md.did
        GROUP BY d.fname
        ORDER BY cnt DESC
        LIMIT 20
        '''
        # SELECT Directors.fname, Directors.lname, COUNT(*) AS cnt
        # FROM Directors
        # INNER JOIN Movie_Director md1 ON md1.did = Directors.did
        # GROUP BY Directors.fname, Directors.lname
        # ORDER BY cnt DESC
        # '''     

        # Q06 ########################          
        cur.execute('DROP VIEW IF EXISTS mCasts')
        cur.execute('DROP VIEW IF EXISTS counts')
        cur.execute('CREATE VIEW mCasts AS SELECT m1.title AS title FROM Movies m1, Cast c1 WHERE m1.mid = c1.mid;')
        cur.execute('CREATE VIEW counts AS SELECT title, COUNT(*) AS cnt FROM mCasts GROUP BY title;')
        queries['q06'] = '''
        SELECT title, cnt
        FROM counts
        ORDER BY cnt DESC
        LIMIT 20
        '''     

        # Q07 ########################
        cur.execute('DROP VIEW IF EXISTS genders')
        cur.execute('DROP VIEW IF EXISTS mCounts')
        cur.execute('CREATE VIEW genders AS SELECT m1.title AS title, Actors.gender AS gender FROM Actors, Movies INNER JOIN Cast c1 on c1.aid = Actors.aid INNER JOIN Movies m1 on c1.mid = m1.mid GROUP BY fname, lname, m1.title;')
        cur.execute('CREATE VIEW mCounts AS SELECT genders.title AS title, SUM(CASE WHEN genders.gender = "Female" THEN 1 ELSE 0 END) AS fem, SUM(CASE WHEN genders.gender = "Male" THEN 1 ELSE 0 END) AS mal FROM genders GROUP BY genders.title;')
        queries['q07'] = '''
        SELECT mCounts.title, mCounts.fem, mCounts.mal
        FROM mCounts
        WHERE mCounts.fem > mCounts.mal
        ORDER BY mCounts.title ASC
        '''     

        # Q08 ########################          
        cur.execute('DROP VIEW IF EXISTS v1')
        cur.execute('DROP VIEW IF EXISTS counts')
        cur.execute('CREATE VIEW v1 AS SELECT a1.fname AS first, a1.lname AS last, a1.aid AS aid, c1.mid AS mid, d1.did AS did FROM Actors a1, Movies m1, Cast c1, Directors d1, Movie_Director md1 WHERE a1.aid = c1.aid AND d1.did=md1.did AND m1.mid = c1.mid AND m1.mid = md1.mid ;')
        cur.execute('CREATE VIEW counts AS SELECT first, last, COUNT(*) AS cnt FROM v1 GROUP BY aid ;')
        queries['q08'] = '''
        SELECT first, last, cnt
        FROM counts
        WHERE cnt >= 6
        '''     

        # Q09 ########################
        cur.execute('DROP VIEW IF EXISTS v2')
        cur.execute('DROP VIEW IF EXISTS debutYear')
        cur.execute('CREATE VIEW v2 AS SELECT a1.fname AS first, a1.lname AS last, a1.aid AS aid, m1.year AS year FROM Actors a1, Movies m1, Cast c1 WHERE first LIKE "S%" AND m1.mid = c1.mid AND a1.aid = c1.aid;')
        cur.execute('CREATE VIEW debutYear AS SELECT first, last, aid, year, Count(*) AS cnt FROM v2 GROUP BY aid, year;')
        queries['q09'] = '''
        SELECT first, last, MIN(year), cnt
        FROM debutYear
        GROUP BY aid
        ORDER BY cnt DESC
        '''     

        # Q10 ########################          
        queries['q10'] = '''
        SELECT Actors.lname, Actors.fname, m1.title
        FROM Actors
        INNER JOIN Cast c1 on c1.aid = Actors.aid
        INNER JOIN Movies m1 on m1.mid = c1.mid
        INNER JOIN Movie_Director md1 on m1.mid = md1.mid
        INNER JOIN Directors d1 on d1.did = md1.did
        WHERE d1.lname = Actors.lname AND d1.fname <> Actors.fname
        '''     

        # Q11 ########################
        cur.execute('DROP VIEW IF EXISTS HanksMovie')
        cur.execute('CREATE VIEW HanksMovie AS SELECT m1.title AS title, m1.mid AS mid FROM Actors INNER JOIN Cast c1 on c1.aid = Actors.aid INNER JOIN Movies m1 on m1.mid = c1.mid INNER JOIN Movie_Director md1 on m1.mid = md1.mid INNER JOIN Directors d1 on d1.did = md1.did WHERE Actors.fname = "Tom" AND Actors.lname = "Hanks";')
        queries['q11'] = '''
        SELECT a2.fname, a2.lname
        FROM HanksMovie
        INNER JOIN Cast c1 on c1.mid = HanksMovie.mid
        INNER JOIN Actors a1 on a1.aid = c1.aid
        INNER JOIN Cast c2 on c2.aid = a1.aid
        INNER JOIN Movies m1 on m1.mid = c2.mid
        INNER JOIN Cast c3 on c3.mid = m1.mid
        INNER JOIN Actors a2 on a2.aid = c3.aid
        WHERE c3.mid != HanksMovie.mid AND a1.aid != c3.aid AND a1.fname != "Tom" AND a1.lname != "Hanks"
        GROUP BY a2.fname, a2.lname
        ORDER BY a2.lname, a2.fname ASC
        '''     

        # Q12 ########################
        cur.execute('DROP VIEW IF EXISTS v3')
        cur.execute('DROP VIEW IF EXISTS v4')
        cur.execute('DROP VIEW IF EXISTS v5')
        cur.execute('CREATE VIEW v3 AS SELECT a1.fname AS first, a1.lname AS last, a1.aid AS aid, m1.rank AS rank FROM Actors a1, Movies m1, Cast c1 WHERE m1.mid = c1.mid AND a1.aid = c1.aid;')
        cur.execute('CREATE VIEW v4 AS SELECT  first, last, aid, Count(*) AS movN, SUM(rank) AS sum  FROM v3 GROUP BY aid;')
        cur.execute('CREATE VIEW v5 AS SELECT  first, last, aid, movN, sum , sum/movN AS AvgRank  FROM v4 GROUP BY aid;')
        queries['q12'] = '''
        SELECT first, last, movN, AvgRank
        FROM v5
        GROUP BY aid
        ORDER BY AvgRank DESC 
        LIMIT 20
        '''     


        ########################################################################                
        ### SAVE RESULTS TO FILES ##############################################
        ########################################################################                
        # DO NOT MODIFY - START         
        for (qkey, qstring) in sorted(queries.items()):
                try:
                        cur.execute(qstring)
                        all_rows = cur.fetchall()
                        
                        print ("=========== ",qkey," QUERY ======================")
                        print (qstring)
                        print ("----------- ",qkey," RESULTS --------------------")
                        for row in all_rows:
                                print (row)
                                print (" ")

                        save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
                        if (save_to_file):
                                with open(qkey+'.csv', 'w') as f:
                                        writer = csv.writer(f)
                                        writer.writerows(all_rows)
                                        f.close()
                                        print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
                                        
                except lite.Error as e:
                        print ("An error occurred:", e.args[0])
                        # DO NOT MODIFY - END
                        
