from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
import markdown


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

    def test_create_post(self):
        # Log in
        self.client.login(username="dan", password="secret")

        # Check response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        # Check if added successfully
        self.assertContains(response, 'added successfully')

        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

    def test_edit_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Log in
        self.client.login(username="dan", password="secret")

        # Check if edit page exists
        response = self.client.get('/admin/blogengine/post/3/')
        self.assertEqual(response.status_code, 200)

        # Edit the post
        response = self.client.post('/admin/blogengine/post/3/', {
            'title': 'My second post',
            'text': 'This is my second blog post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertContains(response, 'changed successfully')

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post.title, 'My second post')
        self.assertEqual(only_post.text, 'This is my second blog post')

    def test_delete_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Log in
        self.client.login(username="dan", password="secret")

        # Delete the post
        response = self.client.post('/admin/blogengine/post/2/delete/', {
            'post': 'yes'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertContains(response, 'deleted successfully')

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 0)


class PostViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://localhost:8000/)'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        self.assertContains(response, post.title)

        # Check the post text is in the response
        self.assertContains(response, markdown.markdown(post.text))

        # Check the post date is in the response
        self.assertContains(response, str(post.pub_date.year))
        self.assertContains(response, post.pub_date.strftime('%b'))
        self.assertContains(response, str(post.pub_date.day))

        # Check that linked is marked up properly
        self.assertContains(response, '<a href="http://localhost:8000/">my first blog post</a>')
