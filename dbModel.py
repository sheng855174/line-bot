from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://kstpgaxwunspii:39ba2c30de5fc7ebe972edd6e8ba6fdcdab1373d923f14189dee6ebc040aaaa5@ec2-174-129-227-146.compute-1.amazonaws.com:5432/d7r6b8n61fqmdg'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserData(db.Model):
    __tablename__ = 'MemberData'
    Id = db.Column(db.Integer, primary_key=True)
    Level = db.Column(db.String(64))
    Name = db.Column(db.String(64))
    SmartPhone = db.Column(db.String(64))
    Time = db.Column(db.String(64))
    Description = db.Column(db.String(512))

    def __init__(self
                 , Level
                 , Name
                 , SmartPhone
                 , Time
                 , Description
                 ):
        self.Level = Level
        self.Name = Name
        self.SmartPhone = SmartPhone
        self.Time = Time
        self.Description = Description


if __name__ == '__main__':
    manager.run()
