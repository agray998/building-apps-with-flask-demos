from flask_testing import TestCase
from application import app, db
from application.models import Tasks, Users
from flask import url_for
from datetime import date

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "sqlite:///test.db",
            WTF_CSRF_ENABLED = False
        )

        return app
    
    def setUp(self):
        sample_user = Users(forename = "John", surname = "Smith")
        sample_task = Tasks(name="Sample Task", description = "A sample task", priority = 1, due = date.today(), user = 1)
        db.create_all()
        db.session.add_all([sample_user, sample_task])
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViewTasks(TestBase):
    def test_get_tasks(self):
        response = self.client.get(url_for('view_tasks'))
        self.assert200(response)
        self.assertIn(b'Sample Task', response.data)

class TestAddUser(TestBase):
    def test_get_add_user(self):
        response = self.client.get(url_for('add_user'))
        self.assert200(response)
        self.assertIn(b'Add User', response.data)
    
    def test_post_add_user(self):
        response = self.client.post(
            url_for('add_user'),
            data = dict(forename = "Bob", surname = "Jones"),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Bob Jones', response.data)
