# connexion
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 2

# redis
TUMBLRS_NAMES = "tumblrs"
POSTS_TOREBLOG = "toreblog" # with tumblr name
POSTS_ONGOING = "ongoing"
POSTS_REBLOGGED = "reblogged"
POSTS_FAILED = "failed"

# queue
QUEUE_TIMEOUT_MINUTES = 30 # max minutes to reblog before the worker is failed
MAX_TOREBLOG = 2

# worker
SLEEP_MIN_MINUTES = 1 # sleep before reblog
SLEEP_MAX_MINUTES = 3

# tumblr
REBLOG_STATE = "queue"
