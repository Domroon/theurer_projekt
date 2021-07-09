import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        db_link = current_app.config['DATABASE']
        current_app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_link}"
        g.db = SQLAlchemy(current_app)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    #if db is not None:
        #db.close()


def init_db():
    db = get_db()
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)