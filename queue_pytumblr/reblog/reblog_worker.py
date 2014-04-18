import random
import time

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis
from queue_pytumblr import ReblogTumblr

class ReblogWorker(ReblogTumblr):

    @classmethod
    def reblog(cls, tumblr_name, post_url):
        post = cls(tumblr_name, post_url)
        return post.reblog_post()
        
    def __init__(self, tumblr_name, post_url): 
        self._init_tumblr()
        self.tumblr_name = tumblr_name
        self.post_url = post_url        

    def reblog_post(self):
        self._rand_sleep()
        result = self._tumblr_reblog()
        self._record_post(result)
        return self.post_url #@todo return id post
     
    def _rand_sleep(self):
        secondes = random.randrange(settings.SLEEP_MIN_MINUTES*60,
            settings.SLEEP_MAX_MINUTES*60)
        time.sleep(secondes)

    def _record_post(self, result):
        posts = PostsRedis(self.tumblr_name)
        if result == self.RESULT_REBLOGGED:
            posts.move_post_url_reblogged(self.post_url)
        else:
            posts.move_post_url_reblogged(self.post_url)
        # @todo : if failed