from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://eklbozojortqrx:d8c89da2d9873d79d783541f03e8aa38f99cfd16ce15106c39d5aaf80e1935a8@ec2-54-221-214-3.compute-1.amazonaws.com:5432/dfgqosf2kto6vk"

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
                 , Level
                 , Name
                 , Phone
                 , Time
                 , Description
                 ):
        self.Level = Level
        self.Name = Name
        self.Phone = Phone
        self.Time = Time
        self.Description = Description


if __name__ == '__main__':
    manager.run()
