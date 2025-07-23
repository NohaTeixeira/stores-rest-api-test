"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically.
and makes sure that it is a new, blank database each time.

"""

from unittest import TestCase
from app import app # inorder to set the test client
from db import db # in order to initialize our db and create our tables.

class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls): #runs one for each test case (@classmethod decorator) while setup runs once for each test method
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  # when we initialize the SQLALCHEMY_DATABASE it will look on the config parameter "SQLALCHEMY_DATABASE_URI" and create a blank db file using the sqlite system in our current directory which will be called data.db will be a new blank sqlfile
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True # when an exception happens in my code, it buble up through the flask and caught by the app.errorhandler
        with app.app_context():  # loads up all the app variable and config and pretends to be run the app. so that everything that interact with our app is able to run as if the app was running
            # Only initialize SQLAlchemy if it hasn't been registered yet
            if "sqlalchemy" not in app.extensions:  # checks if SQLAlchemy has already been initialized in your Flask app before initializing it again.
                db.init_app(app)  # tells SQLALCHEMY instance that it should be now initialize with our app

    # 1. setup the db and give us the test client
    # 2. make sure after each test the database is erased

    def setUp(self): # a method that run before every test
        # Make sure db exists:
        with app.app_context(): #loads up all the app variable and config and pretends to be run the app. so that everything that interact with our app is able to run as if the app was running
            db.create_all() # app will create all our tables (the table exits in models/item.py.
        # get a test client
        self.app = app.test_client #test client app. This allows us to simulate sending HTTP requests without actually running the server.
        self.app_context = app.app_context #This saves the app context so it can be used later in tests. It ensures that everything that interacts with the app behaves as if the app were running

    #1. Configures a temporary database (sqlite:///).
    #2. Activates the app context so Flask features work.
    #3. Initializes SQLAlchemy (db.init_app(app)).
    #4. Creates all database tables (db.create_all()).
    #5. Creates a test client (self.app).

    def tearDown(self): # a method that run after every test
        #data base is blank
        with app.app_context():
            db.session.remove() # delete everything from the current session
            db.drop_all() #removing all our tables in the db, making it blank
