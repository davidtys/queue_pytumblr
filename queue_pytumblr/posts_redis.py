import redis
import copy

from queue_pytumblr import settings


class PostsRedis:

    STATE_NONE = "none"
    STATE_TOREBLOG = "toreblog"
    STATE_ONGOING = "ongoing"
    STATE_REBLOGGED = "reblogged"
    STATE_FAILED = "failed"

    OAUTH_KEY = 'oauth'
    CONSUMER_KEY = 'cons_key'
    CONSUMER_SECRET = 'cons_secret'
    OAUTH_TOKEN = 'oauth_token'
    OAUTH_SECRET = 'oauth_secret'

    @classmethod
    def add_post(cls, tumblr_name, post_url):
        posts = cls(tumblr_name)
        return posts.add_post_url_toreblog(post_url)

    @classmethod
    def add_list_posts(cls, tumblr_name, posts_urls, separator=" "):
        posts = cls(tumblr_name)
        return posts.add_list_posts_urls_toreblog(posts_urls.split(separator))

    @classmethod
    def init_oauth(cls, tumblr_name, consumer_key, consumer_secret, oauth_token, oauth_secret):
        posts = cls(tumblr_name)
        posts.set_oauth(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def __init__(self, tumblr_name):        
        self.tumblr_name = tumblr_name
        self._init_redis()
        if len(tumblr_name)>0:
            self._add_tumblr_name()

    def _init_redis(self):
        self._redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def state_post(self, post_url):
        if self.is_post_toreblog(post_url):
            return self.STATE_TOREBLOG
        if self.is_post_ongoing(post_url):
            return self.STATE_ONGOING
        if self.is_post_reblogged(post_url):
            return self.STATE_REBLOGGED
        if self.is_post_failed(post_url):
            return self.STATE_FAILED
        return self.STATE_NONE

    def tumblrs_names(self):
        return self._redis.smembers(settings.TUMBLRS_NAMES)

    def _add_tumblr_name(self):
        return self._redis.sadd(settings.TUMBLRS_NAMES, self.tumblr_name)

    # --- oauth ---

    def get_oauth_tumblr_name(self):
        return self.tumblr_name + ':' + self.OAUTH_KEY

    def set_oauth(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self._redis.hset(self.get_oauth_tumblr_name(), self.CONSUMER_KEY, consumer_key)
        self._redis.hset(self.get_oauth_tumblr_name(), self.CONSUMER_SECRET, consumer_secret)
        self._redis.hset(self.get_oauth_tumblr_name(), self.OAUTH_TOKEN, oauth_token)
        self._redis.hset(self.get_oauth_tumblr_name(), self.OAUTH_SECRET, oauth_secret)

    def get_consumer_key(self):
        return self._redis.hget(self.get_oauth_tumblr_name(), self.CONSUMER_KEY)

    def get_consumer_secret(self):
        return self._redis.hget(self.get_oauth_tumblr_name(), self.CONSUMER_SECRET)

    def get_oauth_token(self):
        return self._redis.hget(self.get_oauth_tumblr_name(), self.OAUTH_TOKEN)

    def get_oauth_secret(self):
        return self._redis.hget(self.get_oauth_tumblr_name(), self.OAUTH_SECRET)

    def check_oauth(self):
        if not self._redis.exists(self.get_oauth_tumblr_name()):
            raise Exception("oauth doesn't exist for '" + self.get_oauth_tumblr_name() +"'")

    # --- to reblog ---

    def add_list_posts_urls_toreblog(self, posts_urls):
        for post_url in posts_urls:
            count = self.add_post_url_toreblog(post_url)
        return count

    def add_post_url_toreblog(self, post_url):
        if self.state_post(post_url) != self.STATE_NONE:
            return 0
        return self._redis.sadd(self.posts_toreblog_name(), post_url)

    def remove_post_url_toreblog(self, post_url):
        return self._redis.srem(self.posts_toreblog_name(), post_url)

    def posts_urls_toreblog(self):
        return self._redis.smembers(self.posts_toreblog_name())

    def count_posts_toreblog(self):
        return len(self.posts_urls_toreblog())

    def is_post_toreblog(self, post_url):
        if self._redis.sismember(self.posts_toreblog_name(), post_url) == 1:
            return True
        return False

    def getdel_post_url_to_reblog(self):
        return self._redis.spop(self.posts_toreblog_name())

    # --- ongoing ---

    def add_post_url_ongoing(self, post_url):
        return self._redis.sadd(self.posts_ongoing_name(), post_url)

    def remove_post_url_ongoing(self, post_url):
        return self._redis.srem(self.posts_ongoing_name(), post_url)

    def posts_urls_ongoing(self):
        return self._redis.smembers(self.posts_ongoing_name())        

    def count_posts_ongoing(self):
        return len(self.posts_urls_ongoing())

    def is_post_ongoing(self, post_url):
        if self._redis.sismember(self.posts_ongoing_name(), post_url) == 1:
            return True
        return False

    # --- reblogged ---

    def move_post_url_reblogged(self, post_url):
        if self.remove_post_url_ongoing(post_url) == 0:
            raise Exception("post '"+ post_url + "' doesn't exist in ongoing (" + str(self.count_posts_ongoing()) + " posts)")
        return self._redis.sadd(self.posts_reblogged_name(), post_url)

    def remove_post_url_reblogged(self, post_url):
        return self._redis.srem(self.posts_reblogged_name(), post_url)

    def posts_urls_reblogged(self):
        return self._redis.smembers(self.posts_reblogged_name())

    def count_posts_reblogged(self):
        return len(self.posts_urls_reblogged())

    def is_post_reblogged(self, post_url):
        if self._redis.sismember(self.posts_reblogged_name(), post_url) == 1:
            return True
        return False

   # --- failed ---

    def move_post_url_failed(self, post_url):
        if self.remove_post_url_ongoing(post_url) == 0:
            raise Exception("post '"+ post_url + "' doesn't exist in ongoing (" + str(self.count_posts_ongoing()) + " posts)")
        return self._redis.sadd(self.posts_failed_name(), post_url)

    def remove_post_url_failed(self, post_url):
        return self._redis.srem(self.posts_failed_name(), post_url)

    def posts_urls_failed(self):
        return self._redis.smembers(self.posts_failed_name())

    def count_posts_failed(self):
        return len(self.posts_urls_failed())

    def is_post_failed(self, post_url):
        if self._redis.sismember(self.posts_failed_name(), post_url) == 1:
            return True
        return False        

    # --- accessors ---

    def posts_toreblog_name(self):
       return self.tumblr_name + ":" + settings.POSTS_TOREBLOG

    def posts_ongoing_name(self):
       return self.tumblr_name + ":" + settings.POSTS_ONGOING

    def posts_reblogged_name(self):
       return self.tumblr_name + ":" + settings.POSTS_REBLOGGED

    def posts_failed_name(self):
       return self.tumblr_name + ":" + settings.POSTS_FAILED

