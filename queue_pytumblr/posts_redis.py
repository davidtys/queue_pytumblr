import redis
import copy

from queue_pytumblr import settings
from queue_pytumblr import FormatTumblr


class PostsRedis:

    STATE_UNKWNOWN = "unkwnown"
    STATE_TOREBLOG = "toreblog"
    STATE_ONGOING = "ongoing"
    STATE_REBLOGGED = "reblogged"

    @classmethod
    def add_post(cls, post_url):
        posts = cls()
        return posts.add_post_url_toreblog(post_url)

    @classmethod
    def add_list_posts(cls, posts_urls, separator=" "):
        posts = cls()
        return posts.add_list_posts_urls_toreblog(posts_urls.split(separator))

    def __init__(self):
        self._init_redis()

    def _init_redis(self):
        self._redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    # --- accessors ---

    def state_post(self, post_url):
        if self.is_post_toreblog(post_url):
            return self.STATE_TOREBLOG
        if self.is_post_ongoing(post_url):
            return self.STATE_ONGOING
        if self.is_post_reblogged(post_url):
            return self.STATE_REBLOGGED
        return self.STATE_UNKWNOWN

    # --- to reblog ---

    def add_list_posts_urls_toreblog(self, posts_urls):
        for post_url in posts_urls:
            count = self.add_post_url_toreblog(post_url)
        return count

    def add_post_url_toreblog(self, post_url):
        return self._redis.sadd(settings.POSTS_TOREBLOG, FormatTumblr.format_post_url(post_url))

    def remove_post_url_toreblog(self, post_url):
        return self._redis.srem(settings.POSTS_TOREBLOG, post_url)

    def posts_urls_toreblog(self):
        return self._redis.smembers(settings.POSTS_TOREBLOG)

    def count_posts_toreblog(self):
        return len(self.posts_urls_toreblog())

    def is_post_toreblog(self, post_url):
        if self._redis.sismember(settings.POSTS_TOREBLOG, post_url) == 1:
            return True
        return False

    # --- ongoing ---

    def move_list_posts_urls_ongoing(self, posts_urls):
        move_urls = copy.copy(posts_urls)
        for move_url in move_urls:
            self.move_post_url_ongoing(move_url)
        return move_urls

    def move_post_url_ongoing(self, post_url):
        if self.remove_post_url_toreblog(post_url) == 0:
            raise Exception("post '"+ post_url + "' doesn't exist in toreblog (" + str(self.count_posts_toreblog()) + " posts)")
        return self._redis.sadd(settings.POSTS_ONGOING, post_url)

    def remove_post_url_ongoing(self, post_url):
        return self._redis.srem(settings.POSTS_ONGOING, post_url)

    def posts_urls_ongoing(self):
        return self._redis.smembers(settings.POSTS_ONGOING)        

    def count_posts_ongoing(self):
        return len(self.posts_urls_ongoing())

    def is_post_ongoing(self, post_url):
        if self._redis.sismember(settings.POSTS_ONGOING, post_url) == 1:
            return True
        return False

    # --- reblogged ---

    def move_list_posts_urls_reblogged(self, posts_urls):
        move_urls = copy.copy(posts_urls)
        for move_url in move_urls:
            self.move_post_url_reblogged(move_url)
        return move_urls

    def move_post_url_reblogged(self, post_url):
        if self.remove_post_url_ongoing(post_url) == 0:
            raise Exception("post '"+ post_url + "' doesn't exist in ongoing (" + str(self.count_posts_ongoing()) + " posts)")
        return self._redis.sadd(settings.POSTS_REBLOGGED, post_url)

    def remove_post_url_reblogged(self, post_url):
        return self._redis.srem(settings.POSTS_REBLOGGED, post_url)

    def posts_urls_reblogged(self):
        return self._redis.smembers(settings.POSTS_REBLOGGED)

    def count_posts_reblogged(self):
        return len(self.posts_urls_reblogged())

    def is_post_reblogged(self, post_url):
        if self._redis.sismember(settings.POSTS_REBLOGGED, post_url) == 1:
            return True
        return False