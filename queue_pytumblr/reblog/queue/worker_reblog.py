from queue_pytumblr import RedisReblog
from queue_pytumblr import WorkerTumblr
from queue_pytumblr import TumblrReblog


class WorkerReblog(WorkerTumblr):

    @classmethod
    def reblog(cls, tumblr_name, post_url, sleep_before=True):
        post = cls(tumblr_name, post_url, sleep_before)
        return post.do_work()


    def _init_redis(self):
        self._redis = RedisReblog(self.tumblr_name)
        self._redis.check_oauth()
        
    def _init_tumblr(self):
        self._tumblr = TumblrReblog(self.tumblr_name, self.post_url,
            self._redis.get_consumer_key(), self._redis.get_consumer_secret(), 
            self._redis.get_oauth_token(), self._redis.get_oauth_secret())

    def _tumblr_action(self):
        return self._tumblr.reblog_post_url()

    def _tumblr_after(self, id):        
        if not id:
            self._redis.move_post_url_failed(self.post_url)
            pass
        else:
            self._redis.move_post_url_reblogged(self.post_url)
