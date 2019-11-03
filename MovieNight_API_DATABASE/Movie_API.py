from flask import Flask, render_template, jsonify
import requests
import json
import SQLite3 as db

app = Flask(__name__)
API_KEY = "f4e0e21fb13c51cac5654e9f89494b2d"
IMDB_Link = "https://www.imdb.com/title/"


@app.route('/')
def hello_world():
    return "Hi!"


# api to DB
def insert_to_db():
    movie_id = 1
    Genre_holder = []
    Max_id = 200
    image_path = "https://image.tmdb.org/t/p/w500"
    while movie_id != Max_id:
        r = requests.get(
            "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + API_KEY)
        movie_data = r.json()
        if movie_data.get('status_code') != 34:
            for item in movie_data.get('genres'):
                Genre_holder.append(item.get('name'))
            ID = int(movie_data.get('id'))
            title = movie_data.get('title')
            genre = Genre_holder
            overview = movie_data.get('overview') \
                if movie_data.get('overview') != "" else "No Description found for this movie"
            imdb_link = IMDB_Link + movie_data.get('imdb_id')
            poster = image_path + str(movie_data.get('poster_path'))
            release_date = movie_data.get('release_date')
            status = movie_data.get('status')
            db.insert(ID, title, genre, overview, poster, release_date, status, imdb_link)
            Genre_holder = []
        movie_id = movie_id + 1


# api to file
def api_read():
    movie_id = 1
    Genre_holder = []
    Max_id = 15
    image_path = "https://image.tmdb.org/t/p/w500"
    with open('api_data.txt', 'w') as file:
        file.write("[")
        while movie_id != Max_id:
            r = requests.get(
                "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + API_KEY)
            movie_data = r.json()
            if movie_data.get('status_code') != 34:
                for item in movie_data.get('genres'):
                    Genre_holder.append(item.get('name'))
                movie_data = {'id': movie_data.get('id'),
                              'title': movie_data.get('title'),
                              'genre': Genre_holder,
                              'overview': movie_data.get('overview')
                              if movie_data.get('overview') != "" else "No Description found for this movie",
                              'imdb_link': IMDB_Link + movie_data.get('imdb_id'),
                              'poster': image_path + str(movie_data.get('poster_path')),
                              'release_date': movie_data.get('release_date'),
                              'status': movie_data.get('status')
                              }
                Genre_holder = []
                file.write(json.dumps(movie_data))
                if movie_id + 1 != Max_id:
                    file.write(",\n")
            movie_id = movie_id + 1
        file.write("]")


if __name__ == '__main__':
    insert_to_db()
    # db.select('ariel')
    # db.drop_M_TB()
    # db.creat_db()


    #app.run()
