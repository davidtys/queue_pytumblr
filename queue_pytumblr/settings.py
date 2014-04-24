import logging

LOG_NAME = "queue_pytumblr.log"
LOG_LEVEL = logging.INFO

# connexion
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 2

# redis
TUMBLRS_NAMES = "tumblrs"

# worker
SLEEP_MIN_MINUTES = 0 # sleep before reblog
SLEEP_MAX_MINUTES = 0

