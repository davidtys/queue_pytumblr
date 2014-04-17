import random
import time

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis

class ReblogWorker:

    RESULT_REBLOGGED = "reblogged"
    RESULT_FAILED = "failed"

    @classmethod
    def reblog(cls, post_url):
        post = cls(post_url)
        return post.reblog_post()
        
    def __init__(self, post_url): 
        self._init_tumblr()
        self.post_url = post_url        

    def _init_tumblr(self):
        # @todo
        pass

    def reblog_post(self):
        self._rand_sleep()
        result = self._tumblr_reblog()
        self._record_post(result)
        return self.post_url #@todo return id post
     
    def _rand_sleep(self):
        secondes = random.randrange(settings.SLEEP_MIN_MINUTES*60,
            settings.SLEEP_MAX_MINUTES*60)
        time.sleep(secondes)

    def _tumblr_reblog(self):
        # @todo
        # @todo state = queue        
        return self.RESULT_REBLOGGED

    def _record_post(self, result):
        posts = PostsRedis()
        posts.move_post_url_reblogged(self.post_url)
        # @todo : if failed