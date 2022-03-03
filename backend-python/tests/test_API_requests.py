from app import create_app
import json

def test_API_request_movies(client):
    response = client.get("/api/v1.0/movies/")
    assert response.status_code == 200

def test_API_request_genres(client):
    response = client.get("/api/v1.0/genres/")
    assert response.status_code == 200
