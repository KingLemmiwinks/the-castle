from app import app
from unittest import TestCase

client = app.test_client()

def test_questions():
    resp = client.get("/")
    body = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "<button>" in body

def test_story():
    qs = {"place": "Bethlehem"}
    resp = client.get("/story", query_string=qs)
    body = resp.get_data(as_text=True)

    assert resp.status_code == 200
    assert "in Bethlehem" in body 

    
class MadlibsTestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_questions(self):
        resp = self.client.get("/")
        body = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("<button>", body)

    def test_story(self):
        qs = {"place": "Bethlehem"}
        resp = self.client.get("/story", query_string=qs)
        body = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("in Bethlehem", body)