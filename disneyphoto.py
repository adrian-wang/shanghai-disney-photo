#!/usr/bin/env python
# -*- encoding:utf-8 -*-

__author__ = 'Adrian Wang'

import os
import requests
import urllib
from config import tokenId

getPhotoBase = 'https://api.disneyphotopass.com.cn/p/getPhotosByConditions'
dataBase = 'https://www.disneyphotopass.com.cn/'
folder = 'media3'
limit = 20

# TODO headers
getPhotoParams = {
    'tokenId': str(tokenId),
    'sortField': 'shootOn',
    'order': '-1'
}


def download(url):
    if not os.path.exists(folder):
        os.mkdir(folder, 0o755)
    file_name = os.path.join(folder, os.path.split(url)[-1])
    urllib.urlretrieve(url, file_name)
    return file_name


def get_photo_urls_url(page_index, limit):
    getPhotoParams['currentPageIndex'] = str(page_index)
    getPhotoParams['limit'] = str(limit)
    parameter = reduce(
        lambda x, y: x + '&' + y,
        map(lambda x: x + '=' + getPhotoParams[x], getPhotoParams))
    return getPhotoBase + '?' + parameter


def get_photo_urls(photos):
    return [ph['thumbnail']['en1024']['url']
            for ph in filter(lambda p: p and p['enImage'], photos)]


def get_all_photo_urls():
    urls = []
    page = 1
    while page:
        url = get_photo_urls_url(page, limit)
        r = requests.get(url)
        data = r.json()
        if int(data['status']) != 100 and int(data['status']) != 200:
            break

        # TODO extract shot time and date
        photos = data['result']['photos']
        print photos
        if len(photos) == 0:
            break
        [urls.append(u) for u in get_photo_urls(photos)]
        page += 1
    return urls


def get_temp_file_names():
    urls = [dataBase + u for u in get_all_photo_urls()]
    return [download(url) for url in urls]


get_temp_file_names()
