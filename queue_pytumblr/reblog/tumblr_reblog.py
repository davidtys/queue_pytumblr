import pytumblr

import logging
from logging.handlers import RotatingFileHandler


class TumblrReblog:

    def __init__(self, tumblr_name, post_url, consumer_key, consumer_secret, oauth_token, oauth_secret, log_errors="errors.log"): 
        self.tumblr_name = tumblr_name
        self.post_url = post_url
        self._init_logger(log_errors)
        self._init_tumblr(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def _init_logger(self, log_errors):
        self.logger = logging.getLogger()
        formatter = logging.Formatter("%(asctime)s :: " + self.tumblr_name + " :: " + self.post_url 
            + " >> %(message)s")
        file_handler = RotatingFileHandler(log_errors, 'a', 1000000, 1)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)        

    def _init_tumblr(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def reblog_post_url(self):
        infos = self.extract_infos_from_post_url()
        if not infos:
            return ''
        reblog_key = self._get_reblog_key_post(infos['blogname'], infos['id'])
        if not reblog_key:
            return ''

        result = self.client.reblog(self.tumblr_name, id=infos['id'], reblog_key=reblog_key)
        if 'id' in result:
            return result['id']
        return ''

    def extract_infos_from_post_url(self):
        infos = {}
        elements = self.post_url.replace('http://', '').split('/')
        if len(elements)<3:
            self.logger.error("elements from url are not valid " + str(elements))
            return infos
        infos['blogname'] = elements[0].replace('.tumblr.com', '')
        infos['id'] = elements[2]        
        return infos

    def _get_infos_post(self, blogname, id):
         infos = self.client.posts(blogname, id=id)
         if 'posts' in infos and len(infos['posts'])>0:
            return infos['posts'][0]
         self.logger.error("no post in infos " + str(infos))
         return {}

    def _get_reblog_key_post(self, blogname, id):
        infos_post = self._get_infos_post(blogname, id)
        if 'reblog_key' in infos_post:
            return str(infos_post['reblog_key'])
        self.logger.error("no reblog_key in infos_post " + str(infos_post))
        return ''           
