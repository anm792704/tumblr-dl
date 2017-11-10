import os
import urllib

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

    total_posts = blogposts.get('total_posts')
    print("Total posts:", total_posts)
    logging.info("Total posts of %s: %i" % (blogurl, total_posts))

    blog_download_directory =  "./"  + blogurl
    if not os.path.isdir(blog_download_directory):
        os.mkdir(blog_download_directory)

    download_list_filename = "download_list_" + blogurl + ".txt"
    archive_list_filename = "archive_list_" + blogurl + ".txt"
    download_list_filehandle = open(download_list_filename, 'a')

    if Path(archive_list_filename).is_file():
        with open(archive_list_filename, 'r') as archive_list_filehandle_read:
            archive_links = str(archive_list_filehandle_read.readlines()).strip()
    else:
        archive_links = ()

    archive_list_filehandle = open(archive_list_filename, 'a')




    start = 0
    steps = 20
    end = 20
    downloaded = 0
    skipped = 0

    if total_posts < steps:
        steps = total_posts

    while start < total_posts:
        blogposts = client.posts (blogurl, limit=steps, offset=start,  type='photo')
        for x in range (0, steps):
            anz_pics = len(blogposts.get('posts')[x].get('photos'))
            for y in range (0, anz_pics):
                pic_url = str(blogposts.get('posts')[x].get('photos')[y].get('original_size').get('url')).replace('https', 'http').strip()
                if (pic_url not in archive_links):
                    download_list_filehandle.write(pic_url + '\n')
                    archive_list_filehandle.write(pic_url + '\n')
                    print ("URL " + pic_url + " added to download and archive list")
                    logging.debug ("URL " + pic_url + " added to download and archive list")
                    downloaded += 1
                    image_name = pic_url.split('/')[-1]
                    filename = blog_download_directory + "/" + str(image_name)
                    if os.path.isfile(filename):
                        print ("File " + filename + " already exists on filesystem, skip it")
                        logging.warning("File " + filename + "already exists on filesystem, skip it")
                    else:
                        print ("File " + filename + " will be downloaded" )
                        logging.debug ("File " + filename + " will be downloaded" )
                        urllib.request.urlretrieve (pic_url, filename)

                else:
                    print ("URL " + pic_url + " already in archive, skip it")
                    logging.debug("URL " + pic_url + " already in archive, skip it")
                    skipped += 1
        start = start + steps
        end = end + steps

        if end > total_posts:
            end = total_posts
            steps = end - start
            print("anz_posts of <" + str(total_posts) + "> reached, set end to anz_posts, set steps to < " + str(steps) + ">")
            logging.debug("anz_posts of <" + str(total_posts) + "> reached, set end to anz_posts, set steps to < " + str(steps) + ">")
        print ("start: <" + str ( start ) + ">, end: <" + str ( end ) + ">, step: <" + str(steps) + ">")
        logging.debug("start: <" + str ( start ) + ">, end: <" + str ( end ) + ">, step: <" + str(steps) + ">")

    archive_list_filehandle.close()
    download_list_filehandle.close()
    print("Finished parsing of %s" % blogurl)
    logging.info("Finished parsing of %s. Statistic: Files added %d, Files skipped %d" % (blogurl, downloaded, skipped))


