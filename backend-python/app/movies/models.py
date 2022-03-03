from app.db import db, BaseModelMixin
from sqlalchemy.ext.hybrid import hybrid_property
import copy

Movie_Genre = db.Table('Movie_Genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('Movie.movie_id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.genre_id'))
)

class Genre(db.Model, BaseModelMixin):
    __tablename__ = 'Genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    movies = db.relationship("Movie", secondary=Movie_Genre)
    
    def getAllOrderedByName():
        genres = db.session \
            .query(Genre.genre_id, Genre.name) \
            .order_by(Genre.name) \
            .all()
        return genres

    def __init__(self, name, genre_id=None):
        if genre_id:
            self.genre_id = genre_id
        self.name = name
    def __repr__(self):
        return f'Genre({self.name})'
    def __str__(self):
        return f'{self.name}'

class Link(db.Model, BaseModelMixin):
    __tablename__ = 'Link'
    link_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.movie_id'), nullable=False)
    imdb_id = db.Column(db.String(16))
    tmdb_id = db.Column(db.String(16))
    
    def __init__(self, movie_id, imdb_id, tmdb_id, link_id=None):
        if link_id:
            self.link_id = link_id
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id

class Rating(db.Model, BaseModelMixin):
    __tablename__ = 'Rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False) 
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.movie_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    
    def __init__(self, user_id, movie_id, rating, timestamp, rating_id=None):
        if rating_id:
            self.rating_id = rating_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.timestamp = timestamp
    def __repr__(self):
        return f'Rating({self.rating})'
    def __str__(self):
        return f'{self.rating}'

class Tag(db.Model, BaseModelMixin):
    __tablename__ = 'Tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.movie_id'), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def getForMovie(movie_id):
        toReturn = []
        tags = db.session.query(Tag.tag) \
            .join(Movie) \
            .filter(Tag.movie_id == movie_id) \
            .order_by(Tag.tag)
        for item in tags:
            toReturn.append(item.tag)
        return toReturn
    
    def __init__(self, user_id, movie_id, tag, timestamp, tag_id=None):
        if tag_id:
            self.tag_id = tag_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = tag
        self.timestamp = timestamp
    def __repr__(self):
        return f'Tag({self.tag})'
    def __str__(self):
        return f'{self.tag}'

class Movie(db.Model, BaseModelMixin):
    __tablename__ = 'Movie'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    average_rating = db.column_property(db.select(db.func.round(db.func.avg(Rating.rating), 1)).where(Rating.movie_id == movie_id).scalar_subquery())
    
    def getWithLinks(title, genre, tag, sort, show, offset):
        orderColum = db.asc(Movie.title) if sort=='asc' else db.desc(Movie.title)
        all_filters = [Movie.movie_id == Link.movie_id]
        if title:
            all_filters.append(Movie.title.like("%{}%".format(title)))
        if genre:
            all_filters.append((Movie_Genre.c.movie_id == Movie.movie_id) & (Movie_Genre.c.genre_id == Genre.genre_id) & (Movie_Genre.c.genre_id == int(genre)))
        if tag:
            all_filters.append(Movie.movie_id == Tag.movie_id)
            all_filters.append(Tag.tag.like("%{}%".format(tag)))
        if not genre:
            moviesWithLinks = db.session.query(
                    Movie.movie_id, Movie.title, 
                    Link.imdb_id, 
                    Link.tmdb_id, 
                    Movie.average_rating, 
                    db.func.count(Movie.movie_id).over().label("total")
                ) \
                .filter(*all_filters) \
                .group_by(Movie.title) \
                .order_by(orderColum) \
                .offset(offset) \
                .limit(int(show))
        else:
            moviesWithLinks = db.session.query(
                    Movie.movie_id, 
                    Movie.title, 
                    Link.imdb_id, 
                    Link.tmdb_id, 
                    Movie.average_rating,
                    db.func.count(Movie.movie_id).over().label("total") 
                ) \
                .join(Movie_Genre) \
                .filter(*all_filters) \
                .group_by(Movie.title) \
                .order_by(orderColum) \
                .offset(offset) \
                .limit(int(show))
        return moviesWithLinks
    
    def getGenres(movie_id):
        toReturn = []
        genres = db.session.query(Genre.name) \
                .join(Movie_Genre) \
                .filter((Movie_Genre.c.movie_id == Movie.movie_id) & (Movie_Genre.c.genre_id == Genre.genre_id) & (Movie_Genre.c.movie_id == movie_id)) \
                .all()
        for item in genres:
            toReturn.append(item.name)
        return toReturn

    def __init__(self, title, movie_id=None):
        if movie_id:
            self.movie_id = movie_id
        self.title = title
    def __repr__(self):
        return f'Movie({self.title})'
    def __str__(self):
        return f'{self.title}'

