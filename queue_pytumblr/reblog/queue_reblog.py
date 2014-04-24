from redis import Redis
from rq import Queue

from queue_pytumblr import settings_reblog
from queue_pytumblr import RedisReblog
from queue_pytumblr import WorkerReblog
from queue_pytumblr import QueueTumblr


class QueueReblog(QueueTumblr):

    @classmethod
    def add_reblog(cls, tumblr_name, post_url):
        RedisReblog.add_post(tumblr_name, post_url)
        count = cls.reblog(tumblr_name)
        if count == 0:
            print "error to add the post in the queue (perhaps it was already ongoing, or reblogged/failed)"

    @classmethod
    def reblog(cls, tumblr_name):
        queue_posts = cls(tumblr_name)
        return queue_posts.do_queue()


    def queue_name(self):
        return "reblog:" + self.tumblr_name         

    def queue_max(self):
        return settings_reblog.QUEUE_REBLOG_MAX

    def _init_redis(self):
        self._redis = RedisReblog(self.tumblr_name)
        self._redis.check_oauth()

    def _init_queue(self):        
        self._queue = Queue(self.queue_name(), 
            default_timeout=settings_reblog.QUEUE_REBLOG_TIMEOUT * 60, connection=Redis())

    def _ongoing_posts_urls_toreblog(self):
        posts_urls = self._redis.posts_urls_toreblog()
        return self._redis.move_list_posts_urls_ongoing(posts_urls)

    def _check_stop_queue(self):
        if self._redis.count_posts_toreblog() == 0:
            return True
        return False

    def _get_post_url(self):
        post_url = self._redis.getdel_post_url_to_reblog()
        self._redis.add_post_url_ongoing(post_url)
        return post_url

    def _worker_func(self):
        return WorkerReblog.reblog        