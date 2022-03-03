from marshmallow import fields
from app.ext import ma

class MovieSchema(ma.Schema):
    movie_id = fields.Integer(dump_only=True)
    title = fields.String()

class MovieWithLinkSchema(ma.Schema):
    movie_id = fields.Integer(dump_only=True)
    title = fields.String()
    imdb_id = fields.String()
    tmdb_id = fields.String()
    average_rating = fields.Float()
    total = fields.Integer()

class GenreSchema(ma.Schema):
    genre_id = fields.Integer(dump_only=True)
    name = fields.String()

class LinkSchema(ma.Schema):
    link_id = fields.Integer(dump_only=True)
    imdb_id = fields.String()
    tmdb_id = fields.String()

class RatingSchema(ma.Schema):
    rating_id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    rating = fields.Float()
    timestamp = fields.Integer()

class TagSchema(ma.Schema):
    tag_id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    tag = fields.String()
    timestamp = fields.Integer()