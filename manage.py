# class for handling a set of commands
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils.types.choice import ChoiceType
from app import app
from extension import db


migrate = Migrate(app, db)
# create an instance of class that will handle our commands
manager = Manager(app)

# Define the migration command to always be preceded by the word "db"
# Example usage: python manage.py db init
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
