import unittest
from app import create_app, db
from app.models import User, Post, Category, Permission


class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_confirmation_token(self):
        u = User(email='john@example.com', username='john', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        self.assertTrue(u.confirmed)

    def test_reset_password_token(self):
        u = User(email='alice@example.com', username='alice', password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_category_insertion(self):
        Category.insert_categories()
        cats = [c.name for c in Category.query.all()]
        self.assertIn('Technology', cats)
        self.assertIn('Sports', cats)
        self.assertIn('Money', cats)
        self.assertIn('Hot', cats)
        self.assertIn('Entertainment', cats)

    def test_post_creation(self):
        p = Post(title='Test Article', url='http://example.com/test',
                 category='Technology')
        db.session.add(p)
        db.session.commit()
        self.assertIsNotNone(p.id)
        self.assertEqual(p.title, 'Test Article')
