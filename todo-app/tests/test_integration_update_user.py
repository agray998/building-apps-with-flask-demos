from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from application import app, db
from application.models import Tasks, Users
from urllib.request import urlopen
from flask import url_for
from datetime import date, timedelta

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            LIVESERVER_PORT = self.TEST_PORT,
            SQLALCHEMY_DATABASE_URI = "sqlite:///test.db",
            DEBUG = True,
            TESTING = True
        )

        return app

    def setUp(self):
        sample_user = Users(forename="John", surname="Smith")
        sample_task = Tasks(name="Sample Task", description="Blahblahblah", priority=1, due=date.today(), user=1)
        db.create_all()
        db.session.add_all([sample_user, sample_task])
        db.session.commit()

        chrome_opts = webdriver.chrome.options.Options()
        chrome_opts.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path="/snap/bin/chromium.chromedriver", options=chrome_opts)

        self.driver.get(f'http://localhost:{self.TEST_PORT}/update-user/1')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()

class TestUpdateUser(TestBase):
    def test_update_user(self):
        name_field = self.driver.find_element(By.XPATH, '/html/body/div/form/input[2]')
        name_field.clear()
        name_field.send_keys('Robert')
        self.driver.find_element(By.XPATH, '/html/body/div/form/input[4]').click()

        assert Users.query.get(1).forename == "Robert"