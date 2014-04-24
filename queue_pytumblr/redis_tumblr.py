import redis
import copy

from queue_pytumblr import settings
from queue_pytumblr import LogTumblr


class RedisTumblr:

    STATE_NONE = "none"

    OAUTH_KEY = 'oauth'
    CONSUMER_KEY = 'cons_key'
    CONSUMER_SECRET = 'cons_secret'
    OAUTH_TOKEN = 'oauth_token'
    OAUTH_SECRET = 'oauth_secret'


    @classmethod
    def init_oauth(cls, tumblr_name, consumer_key, consumer_secret, oauth_token, oauth_secret):
        posts = cls(tumblr_name)
        posts.set_oauth(consumer_key, consumer_secret, oauth_token, oauth_secret)


    def __init__(self, tumblr_name):        
        self.tumblr_name = tumblr_name
        self._init_logging()
        self._init_redis()
        if len(tumblr_name)>0:
            self._add_tumblr_name()

    def _init_redis(self):
        self._redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def _init_logging(self):
        self._logging = LogTumblr(self.tumblr_name)

    def tumblrs_names(self):
        return self._redis.smembers(settings.TUMBLRS_NAMES)

    def _add_tumblr_name(self):
        return self._redis.sadd(settings.TUMBLRS_NAMES, self.tumblr_name)

    def state_post(self, post_url):
        return self.STATE_NONE

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





 

