from flask import current_app, g
from mysql.connector import connect
from flask.cli import with_appcontext
from .utils.console import print_error, print_success
from .schema import instructions
import click

def get_database():
    try:
        if 'database' not in g:
            g.database = connect(
                host=current_app.config['DATABASE_HOST'],
                password=current_app.config['DATABASE_PASSWORD'],
                user=current_app.config['DATABASE_USER'],
                database=current_app.config['DATABASE']
            )

        g.cursor = g.database.cursor(dictionary=True)

        return g.database, g.cursor
    
    except Exception as exception:
        print_error(f'get_database: {exception}')

def close_database(e=None):
    try:
        database = g.pop('database', None)

        if database is not None: database.close()

    except Exception as exception:
        print_error(f'close_database: {exception}')

def init_database():
    try:
        database, cursor = get_database()

        for instruction in instructions:
            cursor.execute(instruction)
        
        database.commit()

    except Exception as exception:
        print_error(f'init_database: {exception}')

@click.command('init-database')
@with_appcontext
def init_database_command():
    init_database()
    print_success('Database Initialized')

def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)