from datetime import datetime
from http import HTTPStatus

from django.test import TestCase

from .models import Page, Question


class TestIndexPage(TestCase):
    def test_index_page_response(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, HTTPStatus.OK)


class TestPagesAPI(TestCase):
    title = "Title"
    markdown = "Markdown"
    created = datetime.now()
    changed = datetime.now()
    author = None

    def setUp(self):
        p = Page()
        p.title = self.title
        p.markdown = self.markdown
        p.created = self.created
        p.changed = self.changed
        p.author = self.author
        p.save()

    def test_read_existing(self):
        res = self.client.get('/api/pages/1/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, {
            'id': 1,
            'title': self.title,
            'markdown': self.markdown,
            'created': self.created.isoformat(),
            'changed': self.changed.isoformat(),
            'author': self.author,
        })

    def test_read_absent(self):
        res = self.client.get('/api/pages/2/')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)


class TestQuestionsViewSet(TestCase):
    title = "Hello"
    text = "Text"
    posted = True
    answer = "Answer"
    created = datetime.now()
    changed = datetime.now()
    author = None

    def setUp(self):
        q = Question()
        q.title = self.title
        q.text = self.text
        q.posted = self.posted
        q.answer = self.answer
        q.created = self.created
        q.changed = self.changed
        q.author = self.author
        q.save()

    def test_read_existing(self):
        res = self.client.get('/api/questions/1/')
        self.assertEqual(res.status_code, HTTPStatus.OK)
        data = res.json()
        self.assertEqual(data, {
            'id': 1,
            'title': self.title,
            'text': self.text,
            'posted': self.posted,
            'answer': self.answer,
            'created': self.created.isoformat(),
            'changed': self.changed.isoformat(),
            'author': self.author,
        })

    def test_read_absent(self):
        res = self.client.get('/api/questions/2/')
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
