import logging

from queue_pytumblr import settings


class LogTumblr:

    def __init__(self, tumblr_name):        
        self.tumblr_name = tumblr_name
        self._logging = logging
        self._logging.basicConfig(filename=settings.LOG_NAME, level=settings.LOG_LEVEL,
            format="%(asctime)s :: %(levelname)s :: " + self.tumblr_name + " :: %(message)s")

    def log_error(self, global_action, action, message):
        self._logging.error(self._get_action_message(global_action, action, message))

    def log_warning(self, global_action, action, message):
        self._logging.warning(self._get_action_message(global_action, action, message))

    def log_info(self, global_action, action, message):
        self._logging.info(self._get_action_message(global_action, action, message))

    def log_debug(self, global_action, action, message):
        self._logging.debug(self._get_action_message(global_action, action, message))

    def _get_action_message(self, global_action, action, message):
        return global_action + " :: " + action + " :: " + message

    def log_error_post(self, global_action, action, post_url, message):
        self._logging.error(self._get_post_message(global_action, action, post_url, message))

    def log_warning_post(self, global_action, action, post_url, message):
        self._logging.warning(self._get_post_message(global_action, action, post_url, message))

    def log_info_post(self, global_action, action, post_url, message):
        self._logging.info(self._get_post_message(global_action, action, post_url, message))

    def log_debug_post(self, global_action, action, post_url, message):
        self._logging.debug(self._get_post_message(global_action, action, post_url, message))

    def _get_post_message(self, global_action, action, post_url, message):
        return global_action + " :: " + action + " :: " + post_url + " :: " + message    