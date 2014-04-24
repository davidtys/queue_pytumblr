from queue_pytumblr import settings_reblog
from queue_pytumblr import RedisTumblr


class RedisReblog(RedisTumblr):

    STATE_TOREBLOG = "toreblog"
    STATE_ONGOING = "ongoing"
    STATE_REBLOGGED = "reblogged"
    STATE_FAILED = "failed"


    @classmethod
    def add_post(cls, tumblr_name, post_url):
        posts = cls(tumblr_name)
        return posts.add_post_url_toreblog(post_url)

    @classmethod
    def add_list_posts(cls, tumblr_name, posts_urls, separator=" "):
        posts = cls(tumblr_name)
        return posts.add_list_posts_urls_toreblog(posts_urls.split(separator))


    def state_post(self, post_url):
        if self.is_post_toreblog(post_url):
            return self.STATE_TOREBLOG
        if self.is_post_ongoing(post_url):
            return self.STATE_ONGOING
        if self.is_post_reblogged(post_url):
            return self.STATE_REBLOGGED
        if self.is_post_failed(post_url):
            return self.STATE_FAILED
        return self.STATE_NONE

    # --- to reblog ---

    def posts_toreblog_name(self):
       return self.tumblr_name + ":" + settings_reblog.POSTS_TOREBLOG

    def add_list_posts_urls_toreblog(self, posts_urls):
        for post_url in posts_urls:
            count = self.add_post_url_toreblog(post_url)
        return count

    def add_post_url_toreblog(self, post_url):
        if self.state_post(post_url) != self.STATE_NONE:
            return 0
        return self._redis.sadd(self.posts_toreblog_name(), post_url)

    def remove_post_url_toreblog(self, post_url):
        return self._redis.srem(self.posts_toreblog_name(), post_url)

    def posts_urls_toreblog(self):
        return self._redis.smembers(self.posts_toreblog_name())

    def count_posts_toreblog(self):
        return len(self.posts_urls_toreblog())

    def is_post_toreblog(self, post_url):
        if self._redis.sismember(self.posts_toreblog_name(), post_url) == 1:
            return True
        return False

    def getdel_post_url_to_reblog(self):
        return self._redis.spop(self.posts_toreblog_name())

    # --- ongoing ---

    def posts_ongoing_name(self):
       return self.tumblr_name + ":" + settings_reblog.POSTS_ONGOING

    def add_post_url_ongoing(self, post_url):
        return self._redis.sadd(self.posts_ongoing_name(), post_url)

    def remove_post_url_ongoing(self, post_url):
        return self._redis.srem(self.posts_ongoing_name(), post_url)

    def posts_urls_ongoing(self):
        return self._redis.smembers(self.posts_ongoing_name())        

    def count_posts_ongoing(self):
        return len(self.posts_urls_ongoing())

    def is_post_ongoing(self, post_url):
        if self._redis.sismember(self.posts_ongoing_name(), post_url) == 1:
            return True
        return False

    # --- reblogged ---

    def posts_reblogged_name(self):
       return self.tumblr_name + ":" + settings_reblog.POSTS_REBLOGGED

    def move_post_url_reblogged(self, post_url):
        if self.remove_post_url_ongoing(post_url) == 0:
            self._logging.log_warning_post("PostsRedis", "move_post_url_reblogged", post_url, "post didn't exist in ongoing (" + str(self.count_posts_ongoing()) + " posts")
        return self._redis.sadd(self.posts_reblogged_name(), post_url)

    def remove_post_url_reblogged(self, post_url):
        return self._redis.srem(self.posts_reblogged_name(), post_url)

    def posts_urls_reblogged(self):
        return self._redis.smembers(self.posts_reblogged_name())

    def count_posts_reblogged(self):
        return len(self.posts_urls_reblogged())

    def is_post_reblogged(self, post_url):
        if self._redis.sismember(self.posts_reblogged_name(), post_url) == 1:
            return True
        return False

   # --- failed ---

    def posts_failed_name(self):
       return self.tumblr_name + ":" + settings_reblog.POSTS_FAILED

    def move_post_url_failed(self, post_url):        
        if self.remove_post_url_ongoing(post_url) == 0:
            self._logging.log_warning_post("PostsRedis", "move_post_url_failed", post_url, "post didn't exist in ongoing (" + str(self.count_posts_ongoing()) + " posts")
        return self._redis.sadd(self.posts_failed_name(), post_url)

    def remove_post_url_failed(self, post_url):
        return self._redis.srem(self.posts_failed_name(), post_url)

    def posts_urls_failed(self):
        return self._redis.smembers(self.posts_failed_name())

    def count_posts_failed(self):
        return len(self.posts_urls_failed())

    def is_post_failed(self, post_url):
        if self._redis.sismember(self.posts_failed_name(), post_url) == 1:
            return True
        return False        

