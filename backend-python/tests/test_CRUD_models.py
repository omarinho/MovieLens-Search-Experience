import pytest, random, os, time
from app import create_app
from app.db import db
from app.movies.models import *
from flask_sqlalchemy import SQLAlchemy

randomID = random.randint(1000, 1000000)

def delete_orphan_tests(app):
    with app.app_context():
        engine = db.create_engine(os.environ.get("SQLALCHEMY_DATABASE_URI_TEST"), {})
        engine.execute(db.text("DELETE FROM Tag WHERE tag_id >= 1000"))
        engine.execute(db.text("DELETE FROM Rating WHERE rating_id >= 1000"))
        engine.execute(db.text("DELETE FROM Link WHERE link_id >= 1000"))
        engine.execute(db.text("DELETE FROM Genre WHERE genre_id >= 1000"))
        engine.execute(db.text("DELETE FROM Movie WHERE movie_id >= 1000"))

def test_create_movie(app):
    delete_orphan_tests(app)
    with app.app_context():
        movie = Movie(movie_id=randomID, title='Losting Translation ' + str(randomID))
        movie.save()        

def test_read_movie(app):
    with app.app_context():    
        movie = Movie.get_by_id(randomID)
        assert (movie.title == 'Losting Translation ' + str(randomID))

def test_update_movie(app):
    with app.app_context():    
        movie = Movie.get_by_id(randomID)
        movie.title = 'Losting Translation updated ' + str(randomID)
        movie.save()

def test_create_genre(app):
    with app.app_context():
        genre = Genre(genre_id=randomID, name='Horror ' + str(randomID))
        genre.save()        

def test_read_genre(app):
    with app.app_context():    
        genre = Genre.get_by_id(randomID)
        assert (genre.name == 'Horror ' + str(randomID))

def test_update_genre(app):
    with app.app_context():    
        genre = Genre.get_by_id(randomID)
        genre.name = 'Horror updated ' + str(randomID)
        genre.save()

def test_create_link(app):
    with app.app_context():
        link = Link(link_id=randomID, movie_id=randomID, imdb_id=str(randomID), tmdb_id=str(randomID))
        link.save()        

def test_read_link(app):
    with app.app_context():    
        link = Link.get_by_id(randomID)
        assert (link.imdb_id == str(randomID))
        assert (link.tmdb_id == str(randomID))

def test_update_link(app):
    with app.app_context():    
        link = Link.get_by_id(randomID)
        link.imdb_id = '1234567890'
        link.save()

def test_create_rating(app):
    with app.app_context():
        rating = Rating(rating_id=randomID, user_id=randomID, movie_id=randomID, rating=2.5, timestamp=time.time())
        rating.save()        

def test_read_rating(app):
    with app.app_context():    
        rating = Rating.get_by_id(randomID)
        assert (rating.rating == 2.5)

def test_update_rating(app):
    with app.app_context():    
        rating = Rating.get_by_id(randomID)
        rating.rating = 5.0
        rating.save()

def test_create_tag(app):
    with app.app_context():
        tag = Tag(tag_id=randomID, user_id=randomID, movie_id=randomID, tag='Very funny ' + str(randomID), timestamp=time.time())
        tag.save()        

def test_read_tag(app):
    with app.app_context():    
        tag = Tag.get_by_id(randomID)
        assert (tag.tag == 'Very funny ' + str(randomID))

def test_update_tag(app):
    with app.app_context():    
        tag = Tag.get_by_id(randomID)
        tag.tag = 'Very funny updated ' + str(randomID)
        tag.save()

def test_delete_tag(app):
    with app.app_context():
        tag = Tag.get_by_id(randomID)
        tag.delete()

def test_delete_rating(app):
    with app.app_context():
        rating = Rating.get_by_id(randomID)
        rating.delete()

def test_delete_link(app):
    with app.app_context():
        link = Link.get_by_id(randomID)
        link.delete()

def test_delete_genre(app):
    with app.app_context():
        genre = Genre.get_by_id(randomID)
        genre.delete()

def test_delete_movie(app):
    with app.app_context():
        movie = Movie.get_by_id(randomID)
        movie.delete()
