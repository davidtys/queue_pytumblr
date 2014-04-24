# Queue PyTumblr #

Asynchronous reblog a list of Tumblr posts, with RQ and Redis

## Quick Usage


add a post to the reblog list of the tumblr, and create a worker for it :
```
QueueReblog.add_reblog(tumblr_name, post_url)
```

run a worker to reblog the posts in the queue :
```
rqworker reblog:tumblr_name
```

display infos about the posts :
```
InfosReblog.infos(tumblr_name)
```

## Config

You need [pytumblr](https://github.com/tumblr/pytumblr) and [rq](http://python-rq.org/)

**You need to setup oauth**

Please follow the instructions in pytumblr (you can use interactive-console.py)

When you have the oauth tokens, record them for your tumblr with

```
PostsRedis.init_oauth(tumblr_name, consumer_key, consumer_secret, oauth_token, oauth_secret)
```

(you can config different oauths for different tumblrs)


## More

Please note the worker sleeps a random time (see settings.py) before begin reblogging.

Please note by default the redis database is '2' (see settings.py)

The posts and oauth are recorded in redis by the tumblr name, so you can manage different tumblrs in the same time (with a worker by tumblr).

In redis, post urls are moving from *toreblog* to *ongoing* (worker), and then to *reblogged* or *failed*


## To Do

It would be cool to integrate with https://github.com/ui/rq-scheduler to run a periodic worker


## Copyright

MIT, have fun