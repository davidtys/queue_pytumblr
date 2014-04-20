from queue_pytumblr import PostsRedis


class PrintPosts(PostsRedis):

    @classmethod
    def infos_all(cls):
        for tumblr_name in cls.tumblrs():
            posts = cls(tumblr_name)
            posts.print_all()
            print('')

    @classmethod
    def tumblrs(cls):
        posts = cls('')
        return posts.tumblrs_names()

    @classmethod
    def infos(cls, tumblr_name):
        posts = cls(tumblr_name)
        posts.print_all()

    @classmethod
    def toreblog(cls, tumblr_name):
        posts = cls(tumblr_name)
        posts.print_posts_toreblog()     

    @classmethod
    def ongoing(cls, tumblr_name):
        posts = cls(tumblr_name)
        posts.print_posts_ongoing()   

    @classmethod
    def reblogged(cls, tumblr_name):
        posts = cls(tumblr_name)
        posts.print_posts_reblogged()

    def print_all(self):
        print("***")
        print self.tumblr_name
        self.print_toreblog()
        self.print_ongoing()
        self.print_reblogged()
        print("***")  

    def print_toreblog(self):
        print("{} posts to reblog").format(self.count_posts_toreblog())

    def print_ongoing(self):
        print("{} posts on going").format(self.count_posts_ongoing())

    def print_reblogged(self):
        print("{} posts reblogged").format(self.count_posts_reblogged())

    def print_posts_toreblog(self):
        self.print_list_posts_urls(self.posts_urls_toreblog(), "to reblog")

    def print_posts_ongoing(self):
        self.print_list_posts_urls(self.posts_urls_ongoing(), "on going")

    def print_posts_reblogged(self):
        self.print_list_posts_urls(self.posts_urls_reblogged(), "reblogged")  

    def print_list_posts_urls(self, posts_urls, name):
        print("{} posts {}").format(len(posts_urls), name)
        count = 0
        for post_url in posts_urls:
            print "  {}) {}".format(count+1, post_url)
            count += 1

