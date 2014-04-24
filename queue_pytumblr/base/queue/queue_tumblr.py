from rq import Queue


class QueueTumblr:

    def __init__(self, tumblr_name):
        self.tumblr_name = tumblr_name
        self._init_redis()
        self._init_queue()    

    def do_queue(self):
        for count in xrange(self.queue_max()):
            if self._check_stop_queue():
                break
            post_url = self._get_post_url()
            self._queue_worker(post_url)
            print "[{}, {}]".format(self.queue_name(), post_url), 
        return count

    def _queue_worker(self, post_url):        
        self._queue.enqueue_call(
            func = self._worker_func(),
            args = (self.tumblr_name, post_url,)
        )

    def _check_stop_queue(self):
        return False

    def queue_name(self, tumblr_name):
        raise Exception("please define queue_name")

    def queue_max(self):
        raise Exception("please define queue_max")    

    def _init_redis(self):        
        raise Exception("please define _init_redis")

    def _init_queue(self):        
        raise Exception("please define _init_queue")

    def _get_post_url(self):
        raise Exception("please define _get_post_url")    

    def _worker_func(self):
        raise Exception("please define _worker_func")
