import pytumblr


class TumblrReblog:

    def __init__(self, tumblr_name, post_url, consumer_key, consumer_secret, oauth_token, oauth_secret): 
        self.tumblr_name = tumblr_name
        self.post_url = post_url
        self._init_tumblr(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def _init_tumblr(self, consumer_key, consumer_secret, oauth_token, oauth_secret):
        self.client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

    def reblog_post_url(self):
        infos = self.extract_infos_from_post_url()
        print infos
        if not infos:
            return ''
        reblog_key = self._get_reblog_key_post(infos['blogname'], infos['id'])
        print reblog_key
        if not reblog_key:
            return ''

        result = self.client.reblog(self.tumblr_name, id=infos['id'], reblog_key=reblog_key)
        print result
        if 'id' in result:
            return result['id']
        return ''

    def extract_infos_from_post_url(self):
        infos = {}
        elements = self.post_url.replace('http://', '').split('/')
        print elements
        if len(elements)<3:
            return infos
        infos['blogname'] = elements[0].replace('.tumblr.com', '')
        infos['id'] = elements[2]        
        return infos

    def _get_infos_post(self, blogname, id):
         infos = self.client.posts(blogname, id=id)
         if 'posts' in infos and len(infos['posts'])>0:
            return infos['posts'][0]
         return {}

    def _get_reblog_key_post(self, blogname, id):
        infos_post = self._get_infos_post(blogname, id)
        if 'reblog_key' in infos_post:
            return str(infos_post['reblog_key'])
        return ''           
