import pytumblr

from queue_pytumblr import LogTumblr


class TumblrClient:

    def __init__(self, tumblr_name, post_url, consumer_key, consumer_secret, oauth_token, oauth_secret): 
        self.tumblr_name = tumblr_name
        self._init_logging()
        self.post_url = post_url
        self._init_tumblr(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def _init_tumblr(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self._client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)    

    def _init_logging(self):
        self._logging = LogTumblr(self.tumblr_name)

    def extract_elements_from_post_url(self):
        elements = {}
        split_post = self._split_post_url()
        if len(split_post)<3:
            self._logging.log_error_post('TumblrInfos', 'extract_elements_from_post_url', self.post_url, "split_post from url is not valid " + str(split_post))
            return elements
        elements['blogname'] = split_post[0].replace('.tumblr.com', '')
        elements['id'] = split_post[2]        
        return elements

    def _split_post_url(self):
        return self.post_url.replace('http://', '').split('/')

    def _get_infos_post(self, blogname, id):
         infos = self._client.posts(blogname, id=id)
         if 'posts' in infos and len(infos['posts'])>0:
            return infos['posts'][0]
         self._logging.log_error_post('TumblrInfos', '_get_infos_post', self.post_url, "no post in infos " + str(infos))
         return {}
