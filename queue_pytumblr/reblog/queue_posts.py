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
        posts_urls = self._ongoing_posts_urls_toreblog()
        for post_url in posts_urls:
            self.queue_worker_post(post_url)
        return posts_urls

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
