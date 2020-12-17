import unittest
from flask import url_for
from flask_testing import TestCase
from flask_wtf import FlaskForm

from application import app, db
from application.models import Reviews, Games, recommendations_identifier

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            SECRET_KEY='TEST_SECRET_KEY',
            DEBUG=True
        )
        return app

    def setUp(self):
        db.create_all()
        test_review = Reviews(
            author="Test author",
            body="Test body",
            rating = 5
        )
        db.session.add(test_review)
        db.session.commit()
        test_game = Games(
            name = "Test game",
            genre = "Test genre"
        )
        
        test_review.recommendations.append(test_game)
        db.session.add(test_game)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_create_get(self):
        response = self.client.get(url_for('create'))
        self.assertEqual(response.status_code, 200)

    def test_addgame_get(self):
        response = self.client.get(url_for('addgame'))
        self.assertEqual(response.status_code, 200)

    def test_update_get(self):
        response = self.client.get(url_for('update', id=1))
        self.assertEqual(response.status_code, 200)

    def test_delete_get(self):
        response = self.client.get(url_for('delete', id=1))
        self.assertEqual(response.status_code, 302)
    
    def test_deletegame_get(self):
        response = self.client.get(url_for('deletegame', id=1))
        self.assertEqual(response.status_code, 302)

class TestRead(TestBase):
    def test_read_reviews(self):
        response = self.client.get(url_for('home'))
        self.assertIn(b"Test author", response.data)
        self.assertIn(b"Test body", response.data)
        self.assertIn(b"5", response.data)

class TestCreate(TestBase):
    def test_create_review(self):
        response = self.client.post(
            url_for("create"),
            data=dict(
                author="test create author",
                body="test create body",
                rating=4
            ))
        follow_redirects=True
        
        self.assertIn(b"test create author", response.data)
        self.assertIn(b"test create body", response.data)
        self.assertIn(b"4", response.data)

    def test_create_game(self):
        response = self.client.post(
            url_for("addgame"),
            data=dict(
                name="test kunal",
                genre="test genre",
            ))
        follow_redirects=True
        
        self.assertIn(b"test kunal", response.data)
        self.assertIn(b"test genre", response.data)

class TestUpdate(TestBase):
    def test_update_review(self):
        response = self.client.post(
            url_for("update", id=1),
            data=dict(
                body="test update review",
                rating=3,
                game_name = "Test name"
            ),
        follow_redirects=True
        )
        self.assertIn(b"test update review", response.data)
        self.assertIn(b"3", response.data)

    def test_update_game(self):
        response = self.client.post(
            url_for("updategame", id=1),
            data=dict(
                name="test update game",
                genre="test update genre"
            ),
        follow_redirects=True
        )
        self.assertIn(b"test update game", response.data)
        self.assertIn(b"test update genre", response.data)

class TestDelete(TestBase):
    def test_delete_review(self):
        response = self.client.post(
            url_for("delete", id=1),
            follow_redirects=True
        )
        self.assertNotIn(b"Test author", response.data)
        self.assertNotIn(b"Test body", response.data)
    def test_delete_game(self):
        response = self.client.post(
            url_for("deletegame", id=1),
            follow_redirects=True
        )
        self.assertNotIn(b"Test game", response.data)
        self.assertNotIn(b"Test genre", response.data)
