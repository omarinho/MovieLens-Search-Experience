from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from app.db import db
from app.movies.api_v1_0.resources import movies_v1_0_bp
from .ext import ma, migrate
from app.commands import moviesdb
import json, os


def create_app():
    app = Flask(__name__)
    app.config.from_file("../config.json", load=json.load)
    if (app.config['TESTING_MODE']):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_TEST")
        migrationsDir = 'migrations_testing'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        migrationsDir = 'migrations'
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Init extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db, directory=migrationsDir)

    # Disable strict mode for URls with /
    app.url_map.strict_slashes = False
    
    # Register Blueprints
    app.register_blueprint(movies_v1_0_bp)
    app.register_blueprint(moviesdb)
    
    # Register custom error managers  
    register_error_handlers(app)
    return app

def register_error_handlers(app):
    
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405
    
    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403
    
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404