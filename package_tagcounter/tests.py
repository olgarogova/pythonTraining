import unittest
import tagcounter
import sqlite3
import pickle
from unittest import mock


class TestTagcounter(unittest.TestCase):

    def test_parse_html(self):
        res = tagcounter.parse_html("http://127.0.0.1")
        self.assertEqual(res, {'html': 1, 'head': 1, 'meta': 1, 'title': 1, 'style': 1, 'body': 1, 'div': 1, 'a': 1, 'img': 1})

    def test_save_parsed_tags(self):
        dbc = mock.MagicMock()
        url = "http://guimp.com"
        tagcounter.save_parsed_tags(url)

        conn = sqlite3.connect('tagcounter.db')
        c = conn.cursor()
        c.execute("SELECT taglist FROM tags WHERE url = ?", (url,))
        for row in c:
            data = pickle.loads(row[0])
            print(data)
            self.assertEqual(data, {'a': 1, 'body': 1, 'head': 1, 'html': 1, 'img': 1, 'link': 2, 'meta': 10, 'script': 1, 'table': 3, 'td': 3, 'title': 1, 'tr': 3})

        c.execute("DELETE FROM tags WHERE url = ?", (url,))
        conn.commit()
        conn.close()
