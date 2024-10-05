from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text
import os

app = Flask(__name__)

# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')

db = SQLAlchemy(app)

# Create the database tables
from iebank_api.models import Account

with app.app_context():
    # We need to add the db column country to the account table
    """
        query = text("ALTER TABLE account ADD COLUMN country TEXT")
        db.session.execute(query)
        db.session.commit()
    """
    db.create_all()
CORS(app)

from iebank_api import routes
