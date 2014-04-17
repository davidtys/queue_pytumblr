from queue_pytumblr import PostsRedis


class PrintPosts(PostsRedis):

    @classmethod
    def infos(cls):
        posts = cls()
        posts.print_all()

    @classmethod
    def toreblog(cls):
        posts = cls()
        posts.print_posts_toreblog()     

    @classmethod
    def ongoing(cls):
        posts = cls()
        posts.print_posts_ongoing()   

    @classmethod
    def reblogged(cls):
        posts = cls()
        posts.print_posts_reblogged()                      


    def print_all(self):
        print("***")
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

