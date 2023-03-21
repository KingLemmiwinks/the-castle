"""App tests."""

# run these tests like:
# FLASK_ENV=production python -m unittest tests.py

from app import app
from app import get_all_spells, get_spell_detail, add_like_to_db, remove_like_from_db
from flask import session, g
from unittest import TestCase
from models import db, connect_db, User, Likes
from bs4 import BeautifulSoup

CURR_USER_KEY = "curr_user"
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///capstone-test"
app.config['SQLALCHEMY_ECHO'] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
app.config['TESTING'] = True


app.config['WTF_CSRF_ENABLED'] = False


class CapstoneTestCase(TestCase):
    """Tests for the app"""

    def setUp(self):
        """Stuff to do before every test."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        app.config['TESTING'] = True

        self.testuser = User.register("testuser", "testuser")
        db.session.add(self.testuser)
        db.session.commit()

    def test_get_all_spells(self):

        spells = get_all_spells()
        self.assertIsNotNone(spells)

    def test_get_spell_detail(self):

        spell_index = 'acid-arrow'
        spell_detail = get_spell_detail(spell_index)
        self.assertIsNotNone(spell_detail)
        self.assertEqual(spell_index, spell_detail['index'])

    def test_toggle_favorites(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            spell_index = 'acid-arrow'
            spell_name = 'Acid Arrow'
            g.user = self.testuser

            ## ADD LIKE ##

            add_like_to_db(spell_index, spell_name)
            likes = Likes.query.all()
            self.assertIsNotNone(likes)

            ## REMOVE LIKE ##

            remove_like_from_db(spell_index)
            likes = Likes.query.all()
            self.assertEqual(likes, [])


if __name__ == "__main__":
    import doctest
    doctest.testmod()