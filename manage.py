import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool
from app import create_app, db
from app.api.tests import test_create_user


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    db.create_all()
    print("Database initialized")


@manager.command
def drop_db():
    if prompt_bool("Are you sure you want to delete the database?"):
        db.drop_all()
        print("Database dropped!")


@manager.command
def test():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_create_user.FlaskTestCase)
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    manager.run()
