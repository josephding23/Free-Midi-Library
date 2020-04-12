import requests
from requests.utils import CaseInsensitiveDict
import http
from bs4 import BeautifulSoup
import traceback
from random import choice, uniform
import os
from pymongo import MongoClient
import rarfile
import time
import socket
from urllib import request
import mido
import http.cookiejar
import shutil
import re
import hashlib

import http.cookiejar
import shutil
import re
import hashlib

myHeaders = ["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
             "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
             "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
             "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
             "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
             "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
             "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
             "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
             "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
             "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
             "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
             "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
             ]

cookie_str = '__gads=ID=2607f7d39e4e6c2c:T=1586704085:S=ALNI_MZFBAUX0zY7d98Btd_p6v4sOXJ-2w; __utma=44119860.798765121.1586703910.1586703910.1586703910.1;' \
             '__utmb=44119860.3.10.1586703910; __utmc=44119860; __utmz=44119860.1586703910.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' \
             'SERVERID108286=102168|XpMyV|XpMuJ'

cookie_dict = {
    '__gads': 'ID=2607f7d39e4e6c2c:T=1586704085:S=ALNI_MZFBAUX0zY7d98Btd_p6v4sOXJ-2w',
    '__utma': '44119860.798765121.1586703910.1586703910.1586703910.1',
    '__utmb': '44119860.3.10.1586703910',
    '__utmc': '44119860',
    '__utmz': '44119860.1586703910.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    'SERVERID108286': '102168|XpMyV|XpMuJ'
}

cookies = requests.utils.cookiejar_from_dict(cookie_dict=cookie_dict, cookiejar=None, overwrite=True)


def get_jazz_midi_collection():
    client = MongoClient(connect=False)
    return client.jazz_midi.midi


def get_html_text(url, params):
    global attributeErrorNum, httpErrorNum
    try:
        proxy = {'https:': '127.0.0.1:1080', 'http:': '127.0.0.1:1080'}
        r = requests.get(url, proxies=proxy, timeout=10)

        r.headers = params
        r.encoding = 'utf-8'
        status = r.status_code
        if status != 200:
            print('404', url)
            return ''
        return r.text
    # ['HTTPError', 'AttributeError', 'TypeError', 'InvalidIMDB']
    except:
        print(url)
        print(traceback.format_exc())


def acquire_more_jazz():
    midi_collection = get_jazz_midi_collection()

    params = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Cookie': cookie_str,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'www.acroche2.com',
        'Connection': 'keep-alive'
    }

    url = 'http://www.acroche2.com/midi_jazz.html'
    root_url = 'http://www.acroche2.com/'

    text = get_html_text(url, params=params)
    soup = BeautifulSoup(text, 'html.parser')

    pattern = re.compile(r'<li><a href="([\s\S]*)" title="([\s\S]*)">([\s\S]*)</a></li>')

    for item in soup.find_all(name='li'):
        found_item = re.findall(pattern, (str(item)))
        if len(found_item) > 0:
            url = root_url + found_item[0][0]
            name = found_item[0][1]

            midi_collection.insert_one({
                'Name': name,
                'Url': url,
                'Downloaded': False,
                'Transposed': False,
                'MergedAndScaled': False
            })

            print(url)

    # print(len(info))


def download_jazz():
    midi_collection = get_jazz_midi_collection()
    root_dir = 'E:/jazz_midi/raw'

    m = hashlib.md5()

    for midi in midi_collection.find({'Downloaded': False}):
        name = midi['Name']
        url = midi['Url']

        m.update(bytes(name, 'utf-8'))
        md5Value = m.hexdigest()

        params = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Cookie': cookie_str,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'www.acroche2.com',
            'Connection': 'keep-alive'
        }

        r = requests.get(url, params=params)
        print(r.status_code)

        save_path = root_dir + '/' + md5Value + '.mid'

        with open(save_path, 'wb') as f:
            f.write(r.content)
        time.sleep(uniform(0.2, 0.4))
        midi_collection.update_one(
            {'_id': midi['_id']},
            {'$set': {
                'md5': md5Value,
                'Downloaded': True
            }}
        )

        print('Progress: {:.2%}\n'.format(midi_collection.count({'Downloaded': True}) / midi_collection.count()))


if __name__ == '__main__':
    download_jazz()