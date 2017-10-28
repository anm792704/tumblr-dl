import pytumblr
from tumblr_keys import *
from tumblr_url import *
from pathlib import Path
import logging

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret)


logging.basicConfig(filename='tumblr-dl.log',level=logging.INFO, format='%(asctime)s %(message)s')

for blogurl in blogurls:
    blogposts = client.posts(blogurl, type='photo')

    anz_posts = blogposts.get('total_posts')
    print("Total posts:", anz_posts)
    logging.info("Total posts of %s: %i" % (blogurl, anz_posts))


    download_list = "download_list_" + blogurl + ".txt"
    archivelist = "archive_list_" + blogurl + ".txt"
    filehandle_download_list = open(download_list, 'a')

    if Path(archivelist).is_file():
        with open(archivelist, 'r') as filehandle_archivelist_read:
            archive_links = str(filehandle_archivelist_read.readlines()).strip()
    else:
        archive_links = ()

    filehandle_archivelist = open(archivelist, 'a')


    start = 0
    steps = 20
    end = 20
    downloaded = 0
    skipped = 0

    if anz_posts < steps:
        steps = anz_posts

    while start < anz_posts:
        blogposts = client.posts (blogurl, limit=steps, offset=start,  type='photo')
        for x in range (0, steps):
            anz_pics = len(blogposts.get('posts')[x].get('photos'))
            for y in range (0, anz_pics):
                pic_url = str(blogposts.get('posts')[x].get('photos')[y].get('original_size').get('url')).replace('https', 'http').strip()
                if (pic_url not in archive_links):
                    filehandle_download_list.write(pic_url + '\n')
                    filehandle_archivelist.write(pic_url + '\n')
                    print ("URL " + pic_url + " added to download and archive list")
                    logging.debug ("URL " + pic_url + " added to download and archive list")
                    downloaded += 1
                else:
                    print ("URL " + pic_url + " already in archive, skip it")
                    logging.debug("URL " + pic_url + " already in archive, skip it")
                    skipped += 1
        start = start + steps
        end = end + steps

        if end > anz_posts:
            end = anz_posts
            steps = end - start
            print("anz_posts of <" + str(anz_posts) + "> reached, set end to anz_posts, set steps to < " + str(steps) + ">")
            logging.debug("anz_posts of <" + str(anz_posts) + "> reached, set end to anz_posts, set steps to < " + str(steps) + ">")
        print ("start: <" + str ( start ) + ">, end: <" + str ( end ) + ">, step: <" + str(steps) + ">")
        logging.debug("start: <" + str ( start ) + ">, end: <" + str ( end ) + ">, step: <" + str(steps) + ">")

    filehandle_archivelist.close()
    filehandle_download_list.close()
    print("Finished parsing of %s" % blogurl)
    logging.info("Finished parsing of %s. Statistic: Files added %d, Files skipped %d" % (blogurl, downloaded, skipped))


