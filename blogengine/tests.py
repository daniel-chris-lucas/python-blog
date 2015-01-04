from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post


class PostTest(TestCase):
    def test_create_post(self):
        # Create the post
        post = Post()

        # Set the attributes
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()

        # Save
        post.save()

        # Can we find it?
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Check attributes
        self.assertEqual(only_post.title, 'My first post')
        self.assertEqual(only_post.text, 'This is my first blog post')
        self.assertEqual(only_post.pub_date.day, post.pub_date.day)
        self.assertEqual(only_post.pub_date.month, post.pub_date.month)
        self.assertEqual(only_post.pub_date.year, post.pub_date.year)
        self.assertEqual(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEqual(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEqual(only_post.pub_date.second, post.pub_date.second)


class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/login/?next=/admin/')

        # Check response code
        self.assertEqual(response.status_code, 200)

        # Check for 'Log in' in response
        self.assertContains(response, 'Log in')

        # Log the user in
        self.client.login(username="dan", password="secret")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check for 'Log out' in response
        self.assertContains(response, 'Log out')

    def test_logout(self):
        # Log in
        self.client.login(username="dan", password="secret")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertContains(response, 'Log out')

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(response.status_code, 200)

        # Check for 'Log in' in response
        self.assertContains(response, 'Log in')

