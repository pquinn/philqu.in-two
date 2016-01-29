import unittest
from app import app
from flask_testing import TestCase
from flask import session


class RewindrTest(TestCase):

    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def test_get_rewindr_no_session_success(self):
        rv = self.client.get('/rewindr/')
        self.assert_200(rv)
        self.assert_template_used('rewindr/index.html')

    def test_get_rewindr_today_no_session_redirect(self):
        rv = self.client.get('/rewindr/today/')
        self.assert_redirects(rv, '/rewindr/')

    def test_get_rewindr_day_no_session_redirect(self):
        rv = self.client.get('/rewindr/past/')
        self.assert_redirects(rv, '/rewindr/')

    def _test_post_rewindr_with_username(self):
        username = 'phillmatic19'
        rv = app.test_client().post('/rewindr/', data=dict(
            username=username
        ), follow_redirects=False)
        with app.test_request_context():
            self.assertEqual(session.get('username'), username)

    def test_post_rewindr_with_no_username(self):
        rv = app.test_client().post('/rewindr/', data={})
        self.assert_400(rv)


if __name__ == '__main__':
    unittest.main()
