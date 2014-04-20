from redis import Redis
from rq import Queue

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis
from queue_pytumblr import ReblogWorker


class QueuePosts:

    @classmethod
    def add_reblog(cls, tumblr_name, post_url):
        PostsRedis.add_post(tumblr_name, post_url)
        return cls.reblog(tumblr_name)

    @classmethod
    def reblog(cls, tumblr_name):
        queue_posts = cls(tumblr_name)
        return queue_posts.reblog_posts()

    @classmethod
    def queue_name(cls, tumblr_name):
        return tumblr_name 

    def __init__(self, tumblr_name):
        self.tumblr_name = tumblr_name
        self._init_posts_redis()
        self._init_queue()

    # @todo status
    def reblog_posts(self):
        for count in xrange(settings.MAX_TOREBLOG):
            if self._posts.count_posts_toreblog() == 0:
                break
            post_url = self._posts.getdel_post_url_to_reblog()
            self._posts.add_post_url_ongoing(post_url)
            self.queue_worker_post(post_url)
            print "[{}, {}]".format(self.queue_name(self.tumblr_name), post_url), 
        return count

    def _ongoing_posts_urls_toreblog(self):
        posts_urls = self._posts.posts_urls_toreblog()
        return self._posts.move_list_posts_urls_ongoing(posts_urls)

    def queue_worker_post(self, post_url):        
        self.queue.enqueue_call(
            func=ReblogWorker.reblog,
            args=(self.tumblr_name, post_url,))

    def _init_posts_redis(self):
        self._posts = PostsRedis(self.tumblr_name)
        self._posts.check_oauth()

    def _init_queue(self):        
        self.queue = Queue(self.queue_name(self.tumblr_name), 
            default_timeout=settings.QUEUE_TIMEOUT_MINUTES * 60, connection=Redis())
