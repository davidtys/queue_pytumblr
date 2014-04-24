from queue_pytumblr import RedisReblog
from queue_pytumblr import InfosTumblr


class InfosReblog(InfosTumblr):

    @classmethod
    def toreblog(cls, tumblr_name):
        infos = cls(tumblr_name)
        infos.print_posts_toreblog()     

    @classmethod
    def ongoing(cls, tumblr_name):
        infos = cls(tumblr_name)
        infos.print_posts_ongoing()   

    @classmethod
    def reblogged(cls, tumblr_name):
        infos = cls(tumblr_name)
        infos.print_posts_reblogged()

    @classmethod
    def failed(cls, tumblr_name):
        infos = cls(tumblr_name)
        infos.print_posts_failed()        


    def _init_redis(self):
        self._redis = RedisReblog(self.tumblr_name)
        self._redis.check_oauth()

    def print_all(self):
        print("***")
        print self.tumblr_name
        self.print_toreblog()
        self.print_ongoing()
        self.print_reblogged()
        self.print_failed()
        print("***")  

    def print_toreblog(self):
        print("{} posts to reblog").format(self._redis.count_posts_toreblog())

    def print_ongoing(self):
        print("{} posts on going").format(self._redis.count_posts_ongoing())

    def print_reblogged(self):
        print("{} posts reblogged").format(self._redis.count_posts_reblogged())

    def print_failed(self):
        print("{} posts failed").format(self._redis.count_posts_failed())

    def print_posts_toreblog(self):
        self.print_list_posts_urls(self._redis.posts_urls_toreblog(), "to reblog")

    def print_posts_ongoing(self):
        self.print_list_posts_urls(self._redis.posts_urls_ongoing(), "on going")

    def print_posts_reblogged(self):
        self.print_list_posts_urls(self._redis.posts_urls_reblogged(), "reblogged")  

    def print_posts_failed(self):
        self.print_list_posts_urls(self._redis.posts_urls_failed(), "failed")  

    def print_list_posts_urls(self, posts_urls, name):
        print("{} posts {}").format(len(posts_urls), name)
        count = 0
        for post_url in posts_urls:
            print "  {}) {}".format(count+1, post_url)
            count += 1