SELECT name FROM people JOIN stars ON stars.person_id = people.id
WHERE movie_id IN (SELECT DISTINCT(movie_id) FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON stars.movie_id = movies.id WHERE name = "Kevin Bacon" and birth = 1958)
AND name != "Kevin Bacon" GROUP BY name;