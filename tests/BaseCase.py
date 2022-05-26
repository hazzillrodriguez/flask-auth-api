import sys
sys.path.append('..')
from app import create_app
from app.exts import db

import unittest

class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('config.TestConfig')
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()