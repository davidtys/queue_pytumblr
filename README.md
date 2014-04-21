# Queue PyTumblr #

Asynchronous reblog a list of Tumblr posts, with RQ and Redis

## Quick Usage


#### add post to the reblog list of the tumblr, and create a worker for it :
```
QueuePosts.add_reblog(tumblr_name, post_url)
```

####  run workers to reblog the posts in the queue :
```
rqworker tumblr_name
```

####  print infos about the posts :
```
PrintPosts.infos(tumblr_name)
```

## Config

You need [pytumblr](https://github.com/tumblr/pytumblr) and [rq](http://python-rq.org/)

** You need to setup oauth **

Please follow the instructions in pytumblr (a good way is using  interactive-console.py)

When you have the oauth tokens, record them for your tumblr with

```
PostsRedis.init_oauth(tumblr_name, consumer_key, consumer_secret, oauth_token, oauth_secret
```

(you can config different oauths for different tumblrs)


## Tips

Please note the worker sleeps a random time (see settings.py) before begin reblogging. It's to avoid being blocked by Tumblr.

Please note by default the redis database is '2' (see settings.py)

The posts and oauth are recorded in redis by the tumblr name, so you can manage different tumblrs in the same time.

In redis, post urls are moving from *toreblog* to *ongoing* (worker), to *reblogged* or *failed*


## Copyright

MIT, have fun