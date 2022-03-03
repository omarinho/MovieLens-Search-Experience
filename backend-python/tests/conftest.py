import os
import pytest
from app import create_app

def pytest_configure(config):
    app = create_app()
    if not app.config['TESTING_MODE']:
        print("================================================================================")
        print("ERROR: YOU NEED TESTING_MODE AS 'true' in config.json to be able to run testing.")
        print("================================================================================")
        os._exit(1)

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        os.system("flask moviesdb create_tables_testing")
        os.system("flask moviesdb loading_csv --mode testing")
        os.system("flask moviesdb upgrade_tables")
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()