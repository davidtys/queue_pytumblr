import fakeredis

from queue_pytumblr import settings
from queue_pytumblr import PostsRedis

def tumblr_name():
    return "test"

def create_redis(db=0):
    return fakeredis.FakeStrictRedis(db=db)

def create_postsredis(db=0):
    posts = PostsRedis(tumblr_name())
    posts._redis = create_redis(db)
    init_postsredis(posts)
    return posts

def init_postsredis(posts):
    posts._redis.delete(posts.posts_toreblog_name())
    posts._redis.delete(posts.posts_ongoing_name())
    posts._redis.delete(posts.posts_reblogged_name())
    posts._redis.delete(posts.posts_failed_name())


def get_post_url():
    return "http://kubricksfilms.tumblr.com/post/80674960029/space-station-v-from-2001-a-space-odyssey"

def list_posts_urls():
    return ["http://kubricksfilms.tumblr.com/post/80674960029/space-station-v-from-2001-a-space-odyssey",
        "http://kubricksfilms.tumblr.com/post/77272481194/philip-stone-left-jack-nicholson-right-on",
        "http://kubricksfilms.tumblr.com/post/22320813304/kubricks-dream-project"]