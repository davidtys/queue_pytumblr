from queue_pytumblr import settings
from queue_pytumblr import PostsRedis

class ReblogWorker:

    @classmethod
    def reblog(cls, post_url, state=""):
        post = cls(post_url, state)
        return post.reblog_post()
        
    def __init__(self, post_url, state=""): # @todo state = queue
        self._init_tumblr()
        self.post_url = post_url        

    def _init_tumblr(self):
        # @todo prend config de fichier ou redis
        pass

    def reblog_post(self):
        # @todo sleep
        # @todo reblog TUMBLR
        self.record_post()
        return self.post_url #@todo return id post
     
    def record_post(self):
        posts = PostsRedis()
        posts.move_post_url_reblogged(self.post_url)