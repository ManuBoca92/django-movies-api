# django-movies-api
### Netguru task

We'd like you to build simple REST API for us - a basic movie database interacting with external API. Here's full specification of endpoints that we'd like it to have:

* POST /movies:
    * Request body should contain only movie title, and its presence should be validated.
    * Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
    * Request response should include full movie object, along with all data fetched from external API.
* GET /movies:
    * Should fetch list of all movies already present in application database.
    * Additional filtering, sorting is fully optional - but some implementation is a bonus.
* POST /comments:
    * Request body should contain ID of movie already present in database, and comment text body.
    * Comment should be saved to application database and returned in request response.
* GET /comments:
    * Should fetch list of all comments present in application database.
    * Should allow filtering comments by associated movie, by passing its ID.
* GET /top:
    * Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
    * Movies with the same number of comments should have the same position in the ranking.
    * Should require specifying a date range for which statistics should be generated.
    
#### Rules & hints
1. Your goal is to implement REST API in Django, however you're free to use any third-party libraries and database of your choice, but please share your reasoning behind choosing them.
2. At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
3. The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
4. Please dockerize your application and use docker-compose or similar solution.
5. Written application must be hosted and publicly available for us online - we recommend Heroku.

#### Solution
I implemented this task using [Django REST framework](https://www.django-rest-framework.org/) and other third-party libraries as instructed. Please see third party libraries below;
* [drf-writable-nested](https://pypi.org/project/drf-writable-nested/) - is a writable nested helpers for django-rest-framework's serializers. As the name implies, I used it for my nested `MovieDetail` and `Ratings`serializers.

As requested that the application be dockerized and deployed on a cloud platform, preferably Heroku. Here is my application domain https://warm-journey-10447.herokuapp.com already deployed on Heroku and configured with automatica deployments after push to `master` branch.

Here is the heroku setup in case you want you check it out
1. Create an account on heroku and download needed CLI using 
```
brew tap heroku/brew && brew install heroku
```
2. Cretae a new application as explained in heroku documentation.
3. Deploy application`command`
```
$ git push heroku master 
```
*If you get an error message with collectstatic, simply disable it by instructing Heroku to ignore running the manage.py collecstatic command during the deployment process.*
```
$ heroku config:set DISABLE_COLLECTSTATIC=1
```
Then, rerun
```
$ git push heroku master 
```
4. Migrate the database
```
$ heroku run python manage.py migrate
```
5. If all went well, at this stage you can vist the application by
```
heroku open
```

##### GET /movies
To fetch the list of movies, please make a GET request to this endpoint `GET /api/v1/movies`.
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
[
    {
        "id": 206,
        "Title": "Bad Boys",
        "Created_at": "2020-05-07T18:34:46.816412"
    },
    {
        "id": 207,
        "Title": "Good Fellas",
        "Created_at": "2020-05-08T08:09:56.469670"
    }
]
```

##### GET /comments
To fetch the list of comments, please make a GET request to this endpoint `GET /api/v1/commnets`.
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "movie_comment": "yes",
        "created_at": "2020-05-08T07:40:42.510591",
        "movie_id": 206
    },
    {
        "id": 2,
        "movie_comment": "another comment",
        "created_at": "2020-05-08T07:41:37.669280",
        "movie_id": 206
    }
 ]
```

**Filtering**, **search** and **ordering** of querysets were also implemented for both *comments* and *movies* endpoints and can be performed like so:

* To filter by `id` on `/movies` endpoint, it can be done by using query string `/api/v1/movies/?id=[id_number]`
* To filter query by ordering   
`/api/v1/comments/?ordering=[object_field]` for asc   
`/api/v1/movies/?ordering=-[object_field]` for desc
* To filter query by *search*   
`/api/v1/comments/?search=[search_text]`

##### POST /movies
POST requests for movie title tat doesn't exist in the DB is fetched from the external API and request response includes full movie object and is saved to DB. To fetch list of full movie objects `GET /api/v1/movie-details/`
```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 72,
        "Ratings": [
            {
                "Source": "Internet Movie Database",
                "Value": "8.3/10"
            },
            {
                "Source": "Rotten Tomatoes",
                "Value": "97%"
            },
            {
                "Source": "Metacritic",
                "Value": "70/100"
            }
        ],
        "Title": "Good Will Hunting",
        "Year": "1997",
        "Rated": "R",
        "Released": "09 Jan 1998",
        "Runtime": "126 min",
        "Genre": "Drama, Romance",
        "Director": "Gus Van Sant",
        "Writer": "Matt Damon, Ben Affleck",
        "Actors": "Matt Damon, Ben Affleck, Stellan Skarsgård, John Mighton",
        "Plot": "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life.",
        "Language": "English",
        "Country": "USA",
        "Awards": "Won 2 Oscars. Another 22 wins & 60 nominations.",
        "Poster": "https://m.media-amazon.com/images/M/MV5BOTI0MzcxMTYtZDVkMy00NjY1LTgyMTYtZmUxN2M3NmQ2NWJhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
        "Metascore": "70",
        "imdbRating": "8.3",
        "imdbVotes": "817,854",
        "imdbID": "tt0119217",
        "Type": "movie",
        "DVD": "08 Dec 1998",
        "BoxOffice": "N/A",
        "Production": "Miramax Films",
        "Website": "N/A"
    }
]
```

##### POST /comments
A `POST /api/v1/comments/` returns a response like so 
```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 21,
    "movie_comment": "Nice movie",
    "created_at": "2020-03-03T12:23:00",
    "movie_id": 209
}
```

#### /top
Movies are ranked according to their number of comments and to fetch the list `GET /api/v1/top`
```
[
    {
        "movie_id": 206,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 207,
        "total_comments": 2,
        "rank": 3
    },
    {
        "movie_id": 209,
        "total_comments": 3,
        "rank": 2
    }
]
```


#### Project setup



