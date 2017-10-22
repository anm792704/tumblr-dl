import pytumblr
from tumblr_keys import *
from tumblr_url import *

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret)

blogposts = client.posts(blogurl, type='photo')

anz_posts = blogposts.get('total_posts')

f = open('output.txt', 'w')
print("Total posts:", anz_posts)

start = 0
steps = 20
end = 20

if anz_posts < steps:
    steps = anz_posts

while start < anz_posts:
    blogposts = client.posts (blogurl, limit=steps, offset=start,  type='photo')
    for x in range (0, steps):
        anz_pics = len(blogposts.get('posts')[x].get('photos'))
        for y in range (0, anz_pics):
            pic_url_https = blogposts.get('posts')[x].get('photos')[y].get('original_size').get('url')
            f.write(pic_url_https.replace('https', 'http') + '\n')
    start = start + steps
    end = end + steps

    if end > anz_posts:
        end = anz_posts
        steps = end - start
        print("anz_posts of <" + str(anz_posts) + "> reached, set end to anz_posts, set steps to < " + str(steps) + ">")
    print ("start: <" + str ( start ) + ">, end: <" + str ( end ) + ">, step: < " + str(steps) + ">")

