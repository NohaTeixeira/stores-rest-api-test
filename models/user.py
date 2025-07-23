from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password): #definding the properties
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() #saves all changes in the session to the database, the actual writing to db

    @classmethod # This means these methods belong to the class (cls) itself, not to an instance of the class. You can call these methods on the class without creating an object first.
    def find_by_username(cls, username): #Uses the class’s query interface (SQLAlchemy) to filter the database records where the username column equals the given username. first() returns the first matching record or None if no match is found.
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


