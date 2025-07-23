"""
This code is responsible for setting up the database connection and ensuring that the
 required tables are created before handling any incoming requests in a Flask application.

"""

from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()



