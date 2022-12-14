from flask_testing import TestCase
from application import app, db
from application.models import Tasks, Users
from flask import url_for
from datetime import date, timedelta

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

class TestAddTask(TestBase):
    def test_get_add_task(self):
        response = self.client.get(url_for('add_todo'))
        self.assert200(response)
        self.assertIn(b'Add Task', response.data)
    
    def test_post_add_task(self):
        response = self.client.post(
            url_for('add_todo'),
            data = dict(
                name = "Sample 2",
                desc = "Another sample task",
                priority = 2,
                due = date.today() + timedelta(30),
                user = 1
            ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Sample 2', response.data)
        assert Tasks.query.get(2).due == date.today() + timedelta(30)

class TestUpdateUser(TestBase):
    def test_get_update_user(self):
        response = self.client.get(url_for('update_user', id=1))
        self.assert200(response)
        self.assertIn(b'John', response.data)
    
    def test_post_update_user(self):
        response = self.client.post(
            url_for('update_user', id=1),
            data = dict(
                forename = "Sarah",
                surname = "Smith"
            ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Sarah Smith', response.data)

class TestUpdateTask(TestBase):
    def test_get_update_task(self):
        response = self.client.get(url_for('update_task', id=1))
        self.assert200(response)
        self.assertIn(b'Sample Task', response.data)
    
    def test_post_update_task(self):
        response = self.client.post(
            url_for('update_task', id=1),
            data = dict(
                name = "Updated Name",
                desc = "Blahblahblah",
                priority = 2,
                due = date.today() + timedelta(1),
                user = 1
            ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Updated Name', response.data)
        assert Tasks.query.get(1).due == (date.today() + timedelta(1))

class TestDeleteTask(TestBase):
    def test_delete_task(self):
        response = self.client.get(
            url_for('delete_task', id = 1),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertNotIn(b'Sample Task', response.data)
        assert Tasks.query.count() == 0

class TestDeleteUser(TestBase):
    def test_delete_user(self):
        response = self.client.get(
            url_for('delete_user', id = 1),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertNotIn(b'John Smith', response.data)
        assert Users.query.count() == 0
