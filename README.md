# challenge-eng-base

To get the project up and running:

1. Install Docker (https://docs.docker.com/engine/installation/) if it is not installed yet.
2. In a terminal, go to the root directory of the project: "challenge-eng-base-master"
3. Please make sure the "backend-python/tests/" folder has the correct permissions (755). 

This folder contains a 'testing-db.sql' file with an instruction to create a testing database when 
docker containers are started. If the procces cannot read 'testing-db.sql', then
an error is generated.

4. Start the containers by running `docker-compose up backend site`

Starting the backend service automatically will start the `Mariadb` database service
as a dependency. When the containers are run for the first time, two DB instances are
created: "challenge" (the main one) and "testing" (exclusively for unit testing).

5. Create the tables in the main database by running `docker-compose exec backend flask moviesdb create_tables`
6. Load the data in the main database by running `docker-compose exec backend flask moviesdb loading_csv`

The loading script uses the CSV files located in the 'backend-python/csv' folder. This command will take some time
to finish (it took around 20 minutes in my dev Linux machine with Ubuntu 20). You will see a verbose
output of the loading process in the terminal.

7. When the loading procces is finished, please verify in the browser the following URLs:

- http://localhost:8080/api/v1.0/movies/ (API)

- http://localhost:8090/ (Frontend - Search experience)


DETECTING CHANGES IN MODELS
===========================

- If models are modified, the following command will propagate the changes to DB tables:
`docker-compose exec backend flask moviesdb upgrade_tables`

Most of changes should be detected, so you won't need to modify the DB tables manually.

The app uses a migration system that will create an additional table in the DB called "alembic_version".
Please don't delete this table. Also a "migrations/" folder will be created to keep track of 
changes in database.



SEARCH EXPERIENCE (FRONTEND)
============================
- You can filter movies by title, genre and tag. These filters can be combined.
- Please keep in mind the 'filter by title' and 'filter by tag' fields only start to filter with 3 or more characters.
- You can sort the results by title (asc or desc)
- Results are paginated. You can specify how many records to show per page (from 10 up to a maximum of 100).



UNIT TESTING
============
'Pytest' and 'Coverage' packages are installed for unit testing.

I have included a few basic unit testing examples (related to API web requests and CRUD operations for models).

To start unit testing, please change "TESTING_MODE" config value in "backend_python/config.json" to `true`
and restart the containers via docker-compose.

- Enter to the backend container shell via `docker exec -it [BACKEND_CONTAINER_NAME] bash` - 
You can find the [BACKEND_CONTAINER_NAME] by running `docker ps` - It will show all the three 
containers (backend, site and db). The last column is the name of each container.

- Run `pytest -v` insisde the container. All unit testings should run successfully at this time (unit testing uses a 
separate database which is created when containers are run for the first time).

- Run `coverage run -m pytest -v` inside the container. After that, run `coverage report`. 
This will generate a report to know how extensive the unit testing is.

