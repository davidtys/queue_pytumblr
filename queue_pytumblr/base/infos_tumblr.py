from queue_pytumblr import RedisTumblr


class InfosTumblr:

    @classmethod
    def infos_all(cls):
        for tumblr_name in cls.tumblrs():
            infos = cls(tumblr_name)
            infos.print_all()
            print('')

    @classmethod
    def tumblrs(cls):
        infos = cls('')
        return infos.tumblrs_names()

    @classmethod
    def infos(cls, tumblr_name):
        infos = cls(tumblr_name)
        infos.print_all()


    def __init__(self, tumblr_name):        
        self.tumblr_name = tumblr_name
        self._init_redis()

    def _init_redis(self):
        self._redis = RedisTumblr(self.tumblr_name)
        self._redis.check_oauth()

    def print_all(self):
        print("***")
        print self.tumblr_name
        print("***")  

