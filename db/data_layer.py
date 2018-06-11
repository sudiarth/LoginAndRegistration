import json, requests
from sqlalchemy import desc
from db.base import DbManager
from db.models import User, Movie, Like

API_URL = 'http://api.tvmaze.com/search/shows?q={}'
API_URL_MOVIE = 'http://api.tvmaze.com/shows/{}'

def get_request(url):
    response = requests.get(url)
    return json.loads(response.text)

def parse_json_movie(self, obj):
    self.url = obj['show']['url']
    self.api_id = obj['show']['id']
    self.name = obj['show']['name']
    if obj['show']['image'] != 'null':
        self.image = obj['show']['image']['medium']
    else:
        self.image = ''

def create_user(email, name, password):
    db = DbManager()
    user = User()
    user.name = name
    user.email = email
    user.password = password
    return db.save(user)

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_email(email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()

def create_like(user_id, movie_id):
    try:
        db = DbManager()

        movie = db.open().query(Movie).filter(Movie.api_id == movie_id).one()

        like = Like()
        like.user_id = user_id
        like.movie_id = movie.id

        db.save(like)

        return like
    except:
        pass


def delete_like(movie_id):
    try:
        db = DbManager()
        show = db.open().query(Like).filter(Like.id == movie_id).one()
        like = db.delete(show)
        return like
    except:
        raise

def get_like(movie_id):
    db = DbManager()
    return db.open().query(Like).filter(Like.id == movie_id).one()

def get_user_like(user_id):
    try:
        db = DbManager()
        likes = db.open().query(Like).filter(Like.user_id == user_id).order_by(desc(Like.created_at)).all()
        return likes
    except:
        pass

def save_movie_to_db(api_id, url, name, image):

    db = DbManager()
    movie = Movie()
    movie.parse_json(obj)
    movie.api_id = api_id
    movie.url = url
    movie.name = name
    movie.image = image

    return save.db(movie)

def search_movie(query):
    try:
        db = DbManager()
        url = API_URL.format(query)
        data = get_request(url)
        movies = []

        for obj in data:
            try:
                movie = Movie()
                movie.parse_json(obj)
                db.save(movie)
                movies.append(movie)
            except:
                movies.append(movie)

        return movies
    except:
        pass

def search_movie_by_url(url):
    try:
        db = DbManager()
        movie = db.open().query(Movie).filter(Movie.url == url).one()
        return movie
    except:
        pass

def get_movie_by_id(movie_id):
    try:
        db = DbManager()
        movie = db.open().query(Movie).filter(Movie.api_id == movie_id).one()
        return movie
    except:
        pass