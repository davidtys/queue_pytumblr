import random
import time

from queue_pytumblr import settings


class WorkerTumblr:

    def __init__(self, tumblr_name, post_url, sleep_before=True): 
        self.tumblr_name = tumblr_name
        self.post_url = post_url
        self.sleep_before = sleep_before    
        self._init_redis()
        self._init_tumblr()

    def do_work(self):
        self._rand_sleep()
        result = self._tumblr_action()
        self._tumblr_after(result)
        return result
 
    def _rand_sleep(self):
        if not self.sleep_before:
            return
        if settings.SLEEP_MAX_MINUTES == 0:
            return
        secondes = random.randrange(settings.SLEEP_MIN_MINUTES*60,
            settings.SLEEP_MAX_MINUTES*60)
        time.sleep(secondes)

    def _init_redis(self):        
        raise Exception("please define _init_redis")

    def _init_tumblr(self):
        raise Exception("please define _init_tumblr")

    def _tumblr_action(self):
        raise Exception("please define _tumblr_action")

    def _tumblr_after(self, result):
        raise Exception("please define _tumblr_after")

