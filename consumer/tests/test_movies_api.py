import json
import unittest

from api.app import app


class TestMoviesAPI(unittest.TestCase):
    def test_movies_get(self):
        request, response = app.test_client.get('/movies')
        assert response.status == 200
        assert json.loads(response.text).get('count') is not None


if __name__ == '__main__':
    unittest.main()
