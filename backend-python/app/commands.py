import os, csv, click
from flask import Blueprint
from .movies.models import Genre, Link, Movie, Rating, Tag

moviesdb = Blueprint('moviesdb', __name__)

@moviesdb.cli.command('create_tables')
def moviesDBCreate():
    if os.path.exists('./migrations'):
        print("=======================================================================================================================")
        print("ERROR: YOU NEED TO DELETE 'migrations/' FOLDER IN 'backend-python/'. ALSO MAKE SURE DATABASE IS EMPTY (WITHOUT TABLES).")
        print("=======================================================================================================================")
    else:
        os.system("flask db init")
        os.system("flask db migrate -m 'Updating tables structure'")
        os.system("flask db upgrade")
        print("========")
        print("FINISHED")
        print("========")

@moviesdb.cli.command('create_tables_testing')
def moviesDBCreate():
    if os.path.exists('./migrations_testing'):
        print("===========================================================")
        print("SKIPPING TABLES CREATION BECAUSE MIGRATIONS EXIST  ALREADY.")
        print("===========================================================")
    else:
        os.system("flask db init")
        os.system("flask db migrate")
        os.system("flask db upgrade")
        print("========")
        print("FINISHED")
        print("========")

@moviesdb.cli.command('upgrade_tables')
def moviesDBUpgrade():
    os.system("flask db migrate -m 'Updating tables structure'")
    os.system("flask db upgrade")
    print("========")
    print("FINISHED")
    print("========")


@moviesdb.cli.command('loading_csv')
@click.option('--mode')
def moviesDBLoading(mode=''):
    fileSuffix = ''
    if mode is not None:
        fileSuffix = '_' + mode
    if (mode is not None) and os.path.exists('./migrations' + fileSuffix):
        print("======================================================")
        print("SKIPPING LOADING CSV BECAUSE MIGRATIONS EXIST ALREADY.")
        print("======================================================")
        exit()
    elif not os.path.exists('./csv'):
        print("=============================")
        print("ERROR: MISSING FOLDER 'csv/'.")
        print("=============================")
    elif not os.path.exists('./csv/links.csv'):
        print("====================================")
        print("ERROR: MISSING FILE 'csv/links.csv'.")
        print("====================================")
    elif not os.path.exists('./csv/movies.csv'):
        print("=====================================")
        print("ERROR: MISSING FILE 'csv/movies.csv'.")
        print("=====================================")
    elif not os.path.exists('./csv/ratings.csv'):
        print("======================================")
        print("ERROR: MISSING FILE 'csv/ratings.csv'.")
        print("======================================")
    elif not os.path.exists('./csv/tags.csv'):
        print("===================================")
        print("ERROR: MISSING FILE 'csv/tags.csv'.")
        print("===================================")
    else:
        print("============================")
        print("LOADING MOVIES AND GENRES...")
        print("============================")
        with open('./csv/movies' + fileSuffix + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0            
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}')
                    movie = Movie(
                        movie_id=int(row[0]),
                        title=row[1]
                    )
                    movie.save()
                    genresList = row[2].split("|")
                    for elem in genresList:
                        rec = Genre.simple_filter(name=elem)
                        if len(rec) == 0:
                            genre = Genre(name=elem)
                        else:
                            genre = rec[0]
                        genre.movies.append(movie)
                        genre.save()
                    line_count += 1                
            print(f'Processed {line_count} lines.')

        print("================")
        print("LOADING LINKS...")
        print("================")
        with open('./csv/links' + fileSuffix + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0            
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}')
                    link = Link(
                        movie_id=int(row[0]),
                        imdb_id=row[1],
                        tmdb_id=row[2]
                    )
                    link.save()
                    line_count += 1                
            print(f'Processed {line_count} lines.')

        print("==================")
        print("LOADING RATINGS...")
        print("==================")
        with open('./csv/ratings' + fileSuffix + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0            
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}')
                    rating = Rating(
                        user_id=int(row[0]),
                        movie_id=row[1],
                        rating=row[2],
                        timestamp=row[3]
                    )
                    rating.save()
                    line_count += 1                
            print(f'Processed {line_count} lines.')

        print("===============")
        print("LOADING TAGS...")
        print("===============")
        with open('./csv/tags' + fileSuffix + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0            
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]}')
                    tag = Tag(
                        user_id=int(row[0]),
                        movie_id=row[1],
                        tag=row[2],
                        timestamp=row[3]
                    )
                    tag.save()
                    line_count += 1                
            print(f'Processed {line_count} lines.')


        print("========================")
        print("========================")
        print("LOADING PROCESS FINISHED")
        print("========================")
        print("========================")
