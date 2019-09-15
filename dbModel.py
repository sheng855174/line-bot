from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://jmwsmzobgczcti:17582fad1e5b57cf0bd0a2530040657bc30d00ce5ae90ea99d2e46ae04357406@ec2-174-129-27-158.compute-1.amazonaws.com:5432/d9858nlbmqmtfl"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'UserData'

    Id = db.Column(db.Integer, primary_key=True)
    Level = db.Column(db.String(256))
    Name = db.Column(db.String(256))
    Phone = db.Column(db.String(256))
    Time = db.Column(db.String(256))
    Description = db.Column(db.String(256))

    def __init__(self
                 , Id
                 , Level
                 , Name
                 , Phone
                 , Time
                 , Description
                 ):
        self.Id = Id
        self.Level = Level
        self.Name = Name
        self.Phone = Phone
        self.Time = Time
        self.Description = Description


if __name__ == '__main__':
    manager.run()
