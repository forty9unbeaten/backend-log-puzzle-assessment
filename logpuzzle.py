#!/usr/bin/env python3
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""


__author__ = 'Rob Spears (GitHub: Forty9Unbeaten)'

import os
import re
import sys
import argparse
import webbrowser

if sys.version_info[0] < 3:
    print('\n\tGotta use Python 3 for this one...\n')
    sys.exit(1)
else:
    import urllib.request


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # Regular expression matches any string of non-whitespace
    # characters that ends in ".jpg"
    img_file_regex = r'\S*\.jpg'

    # Regular expression to determine if custom sorting is needed
    custom_img_regex = r'-\w*-\w*\.jpg'

    server_name = 'http://{}'.format(filename.split('_')[1])

    with open(filename, 'r') as f:
        log_content = f.read()

    # find all image urls in log file, eliminate duplicates and
    # sort in order, accounting for custom sorting need defined
    # in part C of assignment
    img_urls = re.findall(img_file_regex, log_content)
    need_custom_sort = re.search(custom_img_regex, log_content)

    if need_custom_sort:
        def custom_sort(url):
            url = url.split('-')
            return url[-1]
        img_urls = filter(lambda x: re.search(custom_img_regex, x), img_urls)
        img_urls = sorted(set(img_urls), key=custom_sort)
    else:
        img_urls = sorted(set(img_urls))

    # find all image urls in log file, eliminate duplicates and
    # sort in order

    # concat server name with image url to create full URL
    img_urls = [server_name + img_url for img_url in img_urls]

    return img_urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    path = os.path.abspath(dest_dir)

    # Create specified folder to store downloaded images
    try:
        os.makedirs(path)
        print('\n\t{} folder created at {}\n'.format(dest_dir, path))
    except FileExistsError:
        pass
    except Exception as e:
        print(e)

    # download image files at each URL, store them in created
    # directory and append them to a list that serves as the
    # html <img> tags
    img_tags = []
    print('\tLoading...\n')
    for i, url in enumerate(img_urls):
        try:
            response = urllib.request.urlretrieve(
                url, filename='{}/img{}.jpg'.format(path, i))
            filename = response[0]
            img_tags.append('<img src="{}">'.format(filename))
        except FileExistsError:
            pass
        except Exception as e:
            print('\n\tError: {}'.format(e))
    print('\tDone!\n')

    # create index.html file and write html
    full_html = ['<html>', '<body>', ''.join(img_tags), '</body>', '</html>']
    index_file_path = '{}/index.html'.format(path)
    with open(index_file_path, 'w') as f:
        for tag in full_html:
            f.write('{}\n'.format(tag))

    # prompt for viewing of html file
    user_resp = input(
        '\tAll images have been downloaded successfully.' +
        'Would you like to see the picture?\n\tY/N:')

    # open index.html in new browser tab
    if user_resp.strip().lower() == 'y':
        webpage = 'file://{}'.format(index_file_path)
        webbrowser.open(webpage, new=2)
    else:
        print('\n\tindex.html file location:\t{}'.format(index_file_path))


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
