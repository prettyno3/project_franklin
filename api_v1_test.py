import os
import unittest
from flask import jsonify
 
from api_v1 import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_status_code(self):
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)

    def test_post_user_status_code(self):
        response = self.app.post('/api/users', json={
            "name": "user3"
        })
        self.assertEqual(response.status_code, 200)

    def test_put_user_status_code(self):
        response = self.app.put('/api/users/3', json={
            "id": 3,
            "name": "user3"
        })
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_status_code(self):
        response = self.app.delete('/api/users/3')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()