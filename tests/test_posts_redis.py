import unittest

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis
from helpers_tests import *


class TestPostsRedis(unittest.TestCase):

    def setUp(self):
        self._init_posts()

    def _init_posts(self):
        self.posts = create_postsredis()

    def test_add_post_url_toreblog(self):
        post_url = get_post_url()
        self.assertEqual(self.posts._redis.scard(settings.POSTS_TOREBLOG), 0)

        self.posts.add_post_url_toreblog(post_url)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_TOREBLOG), 1)
        self.assertEqual(self.posts._redis.spop(settings.POSTS_TOREBLOG), post_url)

    def test_move_post_url_ongoing(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_ONGOING), 0)

        self.posts.move_post_url_ongoing(post_url)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_TOREBLOG), 0)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_ONGOING), 1)
        self.assertEqual(self.posts._redis.spop(settings.POSTS_ONGOING), post_url)

    def test_move_post_url_reblogged(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.posts.move_post_url_ongoing(post_url)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_REBLOGGED), 0)

        self.posts.move_post_url_reblogged(post_url)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_ONGOING), 0)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_REBLOGGED), 1)
        self.assertEqual(self.posts._redis.spop(settings.POSTS_REBLOGGED), post_url)

    def test_add_list_posts_urls_toreblog(self):
        list_posts = list_posts_urls()

        self.posts.add_list_posts_urls_toreblog(list_posts)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_TOREBLOG), len(list_posts))

    def test_move_list_posts_urls_ongoing(self):
        list_posts = list_posts_urls()
        self.posts.add_list_posts_urls_toreblog(list_posts)

        self.posts.move_list_posts_urls_ongoing(list_posts)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_TOREBLOG), 0)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_ONGOING), len(list_posts))

    def test_move_list_posts_urls_reblogged(self):
        list_posts = list_posts_urls()
        self.posts.add_list_posts_urls_toreblog(list_posts)
        self.posts.move_list_posts_urls_ongoing(list_posts)
        
        self.posts.move_list_posts_urls_reblogged(list_posts)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_ONGOING), 0)
        self.assertEqual(self.posts._redis.scard(settings.POSTS_REBLOGGED), len(list_posts))

    def test_is_post_toreblog(self):
        post_url = get_post_url()
        self.assertFalse(self.posts.is_post_toreblog(post_url))
        self.posts.add_post_url_toreblog(post_url)
        self.assertTrue(self.posts.is_post_toreblog(post_url))

    def test_is_post_toreblog(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.assertFalse(self.posts.is_post_ongoing(post_url))
        self.posts.move_post_url_ongoing(post_url)
        self.assertTrue(self.posts.is_post_ongoing(post_url))

    def test_is_post_reblogged(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.posts.move_post_url_ongoing(post_url)
        self.assertFalse(self.posts.is_post_reblogged(post_url))
        self.posts.move_post_url_reblogged(post_url)
        self.assertTrue(self.posts.is_post_reblogged(post_url))

    def test_state_post(self):
        post_url = get_post_url()
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_UNKWNOWN)
        self.posts.add_post_url_toreblog(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_TOREBLOG)
        self.posts.move_post_url_ongoing(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_ONGOING)
        self.posts.move_post_url_reblogged(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_REBLOGGED)

if __name__ == '__main__':
    unittest.main()