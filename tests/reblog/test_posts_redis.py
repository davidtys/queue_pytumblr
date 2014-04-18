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
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 0)

        self.posts.add_post_url_toreblog(post_url)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 1)
        self.assertEqual(self.posts._redis.spop(self.posts.posts_toreblog_name()), post_url)

    def test_getdel_post_url_to_reblog(self):
         post_url = get_post_url()
         self.posts.add_post_url_toreblog(post_url)
         self.assertEqual(self.posts.getdel_post_url_to_reblog(), post_url)
     
    def test_add_post_url_ongoing(self):
        post_url = get_post_url()
        self.assertEqual(self.posts._redis.scard(self.posts.posts_ongoing_name()), 0)

        self.posts.add_post_url_ongoing(post_url)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 0)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_ongoing_name()), 1)
        self.assertEqual(self.posts._redis.spop(self.posts.posts_ongoing_name()), post_url)

    def test_move_post_url_reblogged(self):
        post_url = get_post_url()
        self.posts.add_post_url_ongoing(post_url)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_ongoing_name()), 1)

        self.posts.move_post_url_reblogged(post_url)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_ongoing_name()), 0)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_reblogged_name()), 1)
        self.assertEqual(self.posts._redis.spop(self.posts.posts_reblogged_name()), post_url)        

    def test_add_list_posts_urls_toreblog(self):
        list_posts = list_posts_urls()

        self.posts.add_list_posts_urls_toreblog(list_posts)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), len(list_posts))

    def test_is_post_toreblog(self):
        post_url = get_post_url()
        self.assertFalse(self.posts.is_post_toreblog(post_url))
        self.posts.add_post_url_toreblog(post_url)
        self.assertTrue(self.posts.is_post_toreblog(post_url))

    def test_is_post_toreblog(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.assertFalse(self.posts.is_post_ongoing(post_url))
        self.posts.add_post_url_ongoing(post_url)
        self.assertTrue(self.posts.is_post_ongoing(post_url))

    def test_is_post_reblogged(self):
        post_url = get_post_url()
        self.posts.add_post_url_toreblog(post_url)
        self.posts.add_post_url_ongoing(post_url)
        self.assertFalse(self.posts.is_post_reblogged(post_url))
        self.posts.move_post_url_reblogged(post_url)
        self.assertTrue(self.posts.is_post_reblogged(post_url))

    def test_state_post(self):
        post_url = get_post_url()
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_NONE)
        self.posts.add_post_url_toreblog(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_TOREBLOG)
        self.posts.remove_post_url_toreblog(post_url)
        self.posts.add_post_url_ongoing(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_ONGOING)
        self.posts.move_post_url_reblogged(post_url)
        self.assertEqual(self.posts.state_post(post_url), PostsRedis.STATE_REBLOGGED)

    def test_add_post_already_ongoing(self):
        post_url = get_post_url()
        self.posts.add_post_url_ongoing(post_url)

        self.assertEqual(self.posts.add_post_url_toreblog(post_url), 0)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 0)

    def test_add_post_already_reblogged(self):
        post_url = get_post_url()
        self.posts.add_post_url_ongoing(post_url)
        self.posts.move_post_url_reblogged(post_url)

        self.assertEqual(self.posts.add_post_url_toreblog(post_url), 0)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 0)

    def test_add_post_already_failed(self):
        post_url = get_post_url()
        self.posts.add_post_url_ongoing(post_url)
        self.posts.move_post_url_failed(post_url)

        self.assertEqual(self.posts.add_post_url_toreblog(post_url), 0)
        self.assertEqual(self.posts._redis.scard(self.posts.posts_toreblog_name()), 0)


if __name__ == '__main__':
    unittest.main()