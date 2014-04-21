import random
import time

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis
from queue_pytumblr import TumblrReblog


class ReblogWorker:

    @classmethod
    def reblog(cls, tumblr_name, post_url):
        post = cls(tumblr_name, post_url)
        return post.reblog_post()
        
    def __init__(self, tumblr_name, post_url, sleep_before=True): 
        self.tumblr_name = tumblr_name
        self.post_url = post_url
        self.sleep_before = sleep_before

    def reblog_post(self):
        if self.sleep_before:
            self._rand_sleep()
        self._init_reblog()
        id = self._tumblr.reblog_post_url()
        self._record_post(id)
        return id

    def _init_reblog(self):
        self._init_posts_redis()
        self._tumblr = TumblrReblog(self.tumblr_name, self.post_url,
            self._posts.get_consumer_key(), self._posts.get_consumer_secret(), 
            self._posts.get_oauth_token(), self._posts.get_oauth_secret())

    def _init_posts_redis(self):
        self._posts = PostsRedis(self.tumblr_name)
        self._posts.check_oauth()

    def _rand_sleep(self):
        secondes = random.randrange(settings.SLEEP_MIN_MINUTES*60,
            settings.SLEEP_MAX_MINUTES*60)
        time.sleep(secondes)

    def _record_post(self, id):        
        if not id:
            self._posts.move_post_url_failed(self.post_url)
            pass
        else:
            self._posts.move_post_url_reblogged(self.post_url)
