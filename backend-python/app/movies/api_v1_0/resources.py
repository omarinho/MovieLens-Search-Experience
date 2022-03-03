from flask import Blueprint
from flask_restful import Api, Resource, request
from app.db import db
from .schemas import MovieWithLinkSchema, GenreSchema
from ..models import Movie, Genre, Tag

movies_v1_0_bp = Blueprint('movies_v1_0_bp', __name__)
movie_with_link_schema = MovieWithLinkSchema()
genre_schema = GenreSchema()
api = Api(movies_v1_0_bp)

class MovieListResource(Resource):
    def get(self):
        args = request.args
        moviesWithLinks = Movie.getWithLinks(
            args['title'] if 'title' in args else '',
            args['genre'] if 'genre' in args else '',
            args['tag'] if 'sort' in args else '',
            args['sort'] if 'sort' in args else 'asc',
            args['show'] if 'show' in args else '30',
            args['offset'] if 'offset' in args else '0'
        )
        result = movie_with_link_schema.dump(moviesWithLinks, many=True)
        for idx, item in enumerate(result):
            tags = Tag.getForMovie(item['movie_id'])
            result[idx]['tags'] = tags
            genres = Movie.getGenres(item['movie_id'])
            result[idx]['genres'] = genres
        return result

class GenreListResource(Resource):
    def get(self):
        args = request.args
        genres = Genre.getAllOrderedByName()
        result = genre_schema.dump(genres, many=True)
        return result

api.add_resource(MovieListResource, '/api/v1.0/movies/', endpoint='movie_list_resource')
api.add_resource(GenreListResource, '/api/v1.0/genres/', endpoint='genre_list_resource')