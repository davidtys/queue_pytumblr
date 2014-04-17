from redis import Redis
from rq import Queue

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis
from queue_pytumblr import ReblogWorker


class QueuePosts:

    @classmethod
    def reblog(cls):
        queue_posts = cls()
        queue_posts.reblog_posts()

    def __init__(self):
        self._posts = PostsRedis()
        self._init_queue()

    # @todo status
    def reblog_posts(self):
        for count in xrange(settings.MAX_TOREBLOG):
            if self._posts.count_posts_toreblog() == 0:
                break
            post_url = self._posts.getdel_post_url_to_reblog()
            self._posts.add_post_url_ongoing(post_url)
            self.queue_worker_post(post_url)
            print post_url,
        return count

    def _ongoing_posts_urls_toreblog(self):
        posts_urls = self._posts.posts_urls_toreblog()
        return self._posts.move_list_posts_urls_ongoing(posts_urls)

    def queue_worker_post(self, post_url):        
        self.queue.enqueue_call(
            func=ReblogWorker.reblog,
            args=(post_url,))

    def _init_queue(self):        
        self.queue = Queue(settings.QUEUE_NAME, 
            default_timeout=settings.QUEUE_TIMEOUT_MINUTES * 60, connection=Redis())
