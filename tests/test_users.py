import json
import unittest

from pony.orm import db_session
from src import app

from tests.utils.factories import User as UserFake
from src.users.models import User


class TestAPIUser(unittest.TestCase):

    def setUp(self):
        self.user = UserFake().__dict__
        self.test_app = app.test_client()

    def test_get_users(self):
        response = self.test_app.get('/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        with db_session:
            user = User(**self.user)
        user_id = user.id
        response = self.test_app.get('/v1/users/{}'.format(user_id))
        with db_session:
            User[user_id].delete()
        response_body = json.loads(response.data)
        # Get user data, the same sent before
        body = self._get_user_data(response_body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(body, sort_keys=True), json.dumps(self.user, sort_keys=True))

    @db_session
    def test_post_user(self):
        response = self.test_app.post('/v1/users/', data=json.dumps(self.user), headers={'Content-Type': 'application/json'})
        response_body = json.loads(response.data)
        body = self._get_user_data(response_body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.dumps(body, sort_keys=True), json.dumps(self.user, sort_keys=True))
        # Deleting created user
        user_id = response_body['User'].keys()[0]
        User[user_id].delete()

    def _get_user_data(self, response_body):
        """ Get user data without data added by DB and serialization """
        body = response_body['User'].values()[0]
        # Removes fields added by DB
        needless = ('updated_at', 'id')
        for k in needless:
            body.pop(k, None)
        return body

    def test_put_user(self):
        with db_session:
            user = User(**self.user)
        user_id = user.id
        self.user['username'] = 'foo'

        response = self.test_app.put('/v1/users/{}'.format(user_id), data=json.dumps(self.user),
                                      headers={'Content-Type': 'application/json'})

        response_body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        with db_session:
            user = User[user_id]
            # User data chaged
            self.assertNotEquals(response_body['User'], user)
            user.delete()

    def test_delete_user(self):
        with db_session:
            user = User(**self.user)

        response = self.test_app.delete('/v1/users/{}'.format(user.id))

        self.assertEqual(response.status_code, 200)
