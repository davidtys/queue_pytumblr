from queue_pytumblr import TumblrClient


class TumblrReblog(TumblrClient):

    def reblog_post_url(self):
        elements = self.extract_elements_from_post_url()
        if not elements:
            return ''
        reblog_key = self._get_reblog_key_post(elements['blogname'], elements['id'])
        if not reblog_key:
            return ''

        result = self._client.reblog(self.tumblr_name, id=elements['id'], reblog_key=reblog_key)
        if 'id' in result:
            return result['id']
        return ''

    def _get_reblog_key_post(self, blogname, id):
        infos_post = self._get_infos_post(blogname, id)
        if 'reblog_key' in infos_post:
            return str(infos_post['reblog_key'])
        self._logging.log_error_post("TumblrReblog", "_get_reblog_key_post", self.post_url, "no reblog_key in infos_post " + str(infos_post))
        return ''
