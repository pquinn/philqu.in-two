import unittest
import flask
from app import app
from flask_testing import TestCase


class RewindrTest(TestCase):

    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def test_get_rewindr_no_session_success(self):
        rv = self.client.get('/rewindr/')
        self.assert_200(rv)
        self.assert_template_used('index.html')

    def test_get_rewindr_today_no_session_redirect(self):
        rv = self.client.get('/rewindr/today/')
        self.assert_redirects(rv, '/rewindr/')

    def test_get_rewindr_day_no_session_redirect(self):
        rv = self.client.get('/rewindr/past/')
        self.assert_redirects(rv, '/rewindr/')

    def test_post_rewindr_with_username(self):
        username = 'phillmatic19'
        with app.test_client() as client:
            rv = client.post('/rewindr/', data=dict(
                username=username
            ), follow_redirects=False)
            assert flask.session['username'] == 'phillmatic19'

    def test_post_rewindr_with_no_username(self):
        rv = app.test_client().post('/rewindr/', data={})
        self.assert_400(rv)

    def set_username_in_session(self, username):
        return app.test_client().post('/rewindr/', data=dict(
            username=username
        ), follow_redirects=False)


if __name__ == '__main__':
    unittest.main()
