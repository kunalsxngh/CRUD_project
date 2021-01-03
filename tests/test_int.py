import unittest
import time
from flask import url_for
from urllib.request import urlopen

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db
from application.models import Reviews, Games


class TestBase(LiveServerTestCase):
    
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        app.config['SECRET_KEY'] = 'TEST_SECRET_KEY'
        return app


    def setUp(self):
        
        #Set up the test driver
        print("--------------------------NEXT-TEST----------------------------------------------")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        db.drop_all()
        db.create_all()
        
        test_game = Games(
            name = "Test game",
            genre = "Test genre"
        )
        test_review = Reviews(
            author="Test author",
            body="Test body",
            rating = 5,
            game = 1
        )
        db.session.add(test_review)     
        db.session.add(test_game)
        db.session.commit()
        self.driver.get("http://localhost:5000")
        
        #Turn off validation
        app.config['WTF_CSRF_ENABLED'] = False

        def tearDown(self):
            self.driver.quit()
            print("--------------------------END-OF-TEST----------------------------------------------\n\n\n-------------------------UNIT-AND-SELENIUM-TESTS----------------------------------------------")

        
        def test_server_is_up_and_running(self):
            response = urlopen("http://localhost:5000")
            self.assertEqual(response.code, 200)

class TestReviewFunctionality(TestBase):
    def test_review_creation(self):

        # Go to the Create Review page
        self.driver.find_element_by_xpath("/html/body/a[2]").click()
        time.sleep(1)

        # Input the review data into the fields
        self.driver.find_element_by_xpath('//*[@id="author"]').send_keys('Test author')
        self.driver.find_element_by_xpath('//*[@id="body"]').send_keys('Test body')
        self.driver.find_element_by_xpath('//*[@id="rating"]').send_keys(5)
        #Submit
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)

        # Assert that browser redirects to the home page
        assert url_for('home') in self.driver.current_url

        #Test that the review was added to the database and is viewed on the website
        test_review = Reviews.query.filter_by(id=2).first()
        assert test_review.author == "Test author"
        assert test_review.body == "Test body"
        assert test_review.rating == 5
        assert test_review.game == 1
    
    #Test the user can click the update button and come back to the updated edition of their review
    def test_review_update(self):

        #Click the update button
        self.driver.find_element_by_xpath('/html/body/form[1]/input').click()

        self.driver.find_element_by_xpath('//*[@id="body"]').send_keys('Updating the review')
        self.driver.find_element_by_xpath('//*[@id="rating"]').send_keys(1)

        #Submit
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        #Test that the review was added to the database
        test_review = Reviews.query.filter_by(id=1).first()
        assert test_review.body == "Updating the review"
        assert test_review.rating == 1

    def test_review_delete(self):
        self.driver.find_element_by_xpath('/html/body/form[2]/input').click()

        #Test that the review was deleted from the database
        assert Reviews.query.filter_by(id=1).scalar() is None

class TestGameFunctionality(TestBase):

    def test_game_creation(self):
        self.driver.find_element_by_xpath('/html/body/a[3]').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('new game')
        self.driver.find_element_by_xpath('//*[@id="genre"]').send_keys('new genre')    
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

        time.sleep(1)

        assert url_for('home') in self.driver.current_url


        new_game = Games.query.filter_by(id=2).first()
        assert new_game.name == "new game"
        assert new_game.genre ==  "new genre"

    def test_game_update(self):

        self.driver.find_element_by_xpath('/html/body/form[3]/input').click()

        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys('updating name')
        self.driver.find_element_by_xpath('//*[@id="genre"]').send_keys('updating genre')

        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        
        update_game = Games.query.filter_by(id=1).first()
        assert update_game.name == "updating name"
        assert update_game.genre ==  "updating genre"


    def test_game_delete(self):
        self.driver.find_element_by_xpath('/html/body/form[4]/input').click()

        assert Games.query.filter_by(id=1).scalar() is None
        

if __name__ == '__main__':
    unittest.main(port=5000)
