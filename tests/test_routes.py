import unittest
from app import create_app, db
from app.models import User, Post, Category


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Category.insert_categories()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News Collection', response.data)

    def test_category_filter(self):
        p = Post(title='Tech News 1', url='http://example.com/tech1',
                 category='Technology')
        db.session.add(p)
        db.session.commit()
        response = self.client.get('/?category=Technology')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tech News 1', response.data)

    def test_auth_pages_render(self):
        for route in ['/auth/login', '/auth/register', '/auth/reset']:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200)

    def test_login_and_subscribe(self):
        u = User(email='testroute@example.com', username='testroute',
                 password='password123', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # Login
        login_res = self.client.post(
            '/auth/login', data={'email': 'testroute@example.com', 'password': 'password123'}, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)

        # Access subscribe
        sub_res = self.client.get('/subscribe/')
        self.assertEqual(sub_res.status_code, 200)
        self.assertIn(b'Column Subscription', sub_res.data)

        # Update subscriptions
        update_res = self.client.post(
            '/subscribe/', data={'column1': 'Technology', 'column2': 'Sports', 'column3': 'Hot'}, follow_redirects=True)
        self.assertEqual(update_res.status_code, 200)
        self.assertIn(b'Subscription has updated!', update_res.data)
