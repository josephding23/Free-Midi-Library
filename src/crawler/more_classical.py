import requests
from requests.utils import CaseInsensitiveDict
import http
from bs4 import BeautifulSoup
import traceback
from random import choice, uniform
import os
import re
from pymongo import MongoClient

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


def get_classical_performer_collection():
    client = MongoClient(connect=False)
    return client.classical_midi.performers


def get_classical_midi_collection():
    client = MongoClient(connect=False)
    return client.classical_midi.midi


def get_html_text(url, params):
    global attributeErrorNum, httpErrorNum
    try:
        proxy = {'https:': '127.0.0.1:1080', 'http:': '127.0.0.1:1080'}
        r = requests.get(url, proxies=proxy)

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


def acquire_more_classical():
    composer_dict = {}

    performer_collection = get_classical_performer_collection()
    midi_collection = get_classical_midi_collection()

    url = 'http://midi.midicn.com/2000/06/06/%E5%8F%A4%E5%85%B8%E9%9F%B3%E4%B9%90MIDI'
    text = get_html_text(url, {'User-Agent': choice(myHeaders)})
    soup = BeautifulSoup(text, 'html.parser')
    pattern = re.compile(r'<li><a href="([\s\S]*)">([\s\S]*)</a>--([\s\S]*)\((\d+)K\)<br/></li>')
    for item in soup.find_all(name='li'):
        found_item = re.findall(pattern, (str(item)))
        if len(found_item) == 0:
            continue
        info = found_item[0]

        midi_url = info[0].strip()
        name = info[1].strip()
        composer_name = info[2].strip()

        midi_collection.insert_one({
            'Name': name,
            'Composer': composer_name,
            'Url': midi_url,
            'Downloaded': False
        })

        if composer_name not in composer_dict.keys():
            composer_dict[composer_name] = {
                'Name': composer_name,
                'WorksNum': 1,
                'Works': [name],
                'WorksUrl': [midi_url]
            }
        else:
            composer_dict[composer_name]['WorksNum'] += 1
            composer_dict[composer_name]['Works'].append(name)
            composer_dict[composer_name]['WorksUrl'].append(midi_url)

    for _, item in composer_dict.items():
        performer_collection.insert_one(item)


def download_classical():
    midi_collection = get_classical_midi_collection()
    root_dir = 'E:/classical_midi'

    m = hashlib.md5()

    for midi in midi_collection.find({'Downloaded': False}):
        name = midi['Name']
        composer = midi['Composer']
        url = midi['Url']

        m.update(bytes(name + ' - ' + composer, 'utf-8'))
        md5Value = m.hexdigest()

        r = requests.get(url)

        save_path = root_dir + '/' + md5Value + '.mid'

        with open(save_path, 'wb') as f:
            f.write(r.content)

        midi_collection.update_one(
            {'_id': midi['_id']},
            {'$set': {
                'md5': md5Value,
                'Downloaded': True
            }}
        )

        print('Progress: {:.2%}\n'.format(midi_collection.count({'Downloaded': True}) / midi_collection.count()))


if __name__ == '__main__':
    download_classical()