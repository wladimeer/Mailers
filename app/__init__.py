import os
from flask import Flask
from .database import init_app
from .email import blueprint_email

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.environ.get('DATABASE'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_USER=os.environ.get('DATABASE_USER'),
        DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD'),
        SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY'),
        DATABASE_HOST=os.environ.get('DATABASE_HOST'),
        FROM_EMAIL=os.environ.get('FROM_EMAIL')
    )

    init_app(app)

    app.register_blueprint(blueprint_email)

    return app