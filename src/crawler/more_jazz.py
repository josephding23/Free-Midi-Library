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
import pretty_midi
import mido
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

cookie_str = '__gads=ID=2607f7d39e4e6c2c:T=1586704085:S=ALNI_MZFBAUX0zY7d98Btd_p6v4sOXJ-2w; __utma=44119860.798765121.1586703910.1586703910.1586741836.2;' \
             '__utmb=44119860.1.10.1586741836; __utmc=44119860; __utmz=44119860.1586703910.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' \
             'SERVERID108286=102168|XpPCZ|XpPCS;__utmt=1'




def get_jazz_midi_collection():
    client = MongoClient(connect=False)
    return client.jazz_midi.midi


def get_midkar_jazz_collection():
    client = MongoClient(connect=False)
    return client.jazz_midikar.midi


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


def acquire_more_jazz_acroche():
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


def acquire_more_jazz_midkar():
    midi_collection = get_midkar_jazz_collection()
    root_url = 'http://midkar.com/jazz'

    crawled_item = []

    m = hashlib.md5()

    for page in range(1, 14):

        source_url = 'http://midkar.com/jazz/jazz_' + str(page).zfill(2) + '.html'
        cookie_str = 'BX=eotmd2df96b5h&b=3&s=m6;sc_is_visitor_unique=rx4375018.1586790157.2B1E41CF9BB14F4C4B3988AFC774B3DD.2.2.2.2.2.2.1.1.1'

        params = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Cookie': cookie_str,
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'www.acroche2.com',
            'Connection': 'keep-alive',
            'Referer': source_url
        }

        text = get_html_text(source_url, params=params)
        soup = BeautifulSoup(text, 'html.parser')

        pattern = re.compile(r'<a href="(.*).mid">(.*)</a>(<br/>|</b></td>)')

        for item in soup.find_all(name='tr'):
            # print(str(item), end='\n\n')
            found_item = re.findall(pattern, (str(item)))

            if len(found_item) != 0:
                crawled_item.append(found_item)
                print(found_item[0])

                name = found_item[0][1]
                url = root_url + '/' + found_item[0][0] + '.mid'

                print(name, '\n', url, '\n')

                m.update(bytes(url, 'utf-8'))
                md5Value = m.hexdigest()


                midi_collection.insert_one({
                    'Url': url,
                    'Name': name,
                    'SourcePage': source_url,
                    'md5': md5Value,
                    'Downloaded': False
                })


    print(len(crawled_item))
    # print(soup)


def download_jazz_achroche():
    midi_collection = get_jazz_midi_collection()
    root_dir = 'E:/jazz_midi/raw'
    socket.setdefaulttimeout(3)


    m = hashlib.md5()
    params = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Cookie': cookie_str,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'www.acroche2.com',
        'Referer': 'http://www.acroche2.com/midi_jazz.html',
        'Proxy-Connection': 'keep-alive'
    }

    cookie_dict = {
        '__gads': 'ID=2607f7d39e4e6c2c:T=1586704085:S=ALNI_MZFBAUX0zY7d98Btd_p6v4sOXJ-2w',
        '__utma': '44119860.798765121.1586703910.1586703910.1586741836.2',
        '__utmb': '44119860.2.10.1586741836',
        '__utmc': '44119860',
        '__utmz': '44119860.1586703910.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        'SERVERID108286': '102168|XpPE9|XpPCS'
    }

    cookies = requests.utils.cookiejar_from_dict(cookie_dict=cookie_dict, cookiejar=None, overwrite=True)

    session = requests.Session()
    requests.packages.urllib3.disable_warnings()
    session.headers.update(params)
    session.cookies = cookies

    for midi in midi_collection.find({'Downloaded': False}):
        name = midi['Name']
        url = midi['Url'][24:]
        url = midi['Url']

        m.update(bytes(name, 'utf-8'))
        md5Value = m.hexdigest()

        try:

            save_path = root_dir + '/' + md5Value + '.mid'

            with open(save_path, 'wb') as output:
                r = session.get(url, verify=False, timeout=20)
                output.write(r.content)

                if r.cookies.get_dict():
                    print(r.cookies.get_dict())
                    session.cookies = r.cookies
                if r.status_code != 200:
                    print('connection error ' + str(r.status_code))

            time.sleep(uniform(0.2, 0.4))

            try:
                pm = pretty_midi.PrettyMIDI(save_path)

                midi_collection.update_one(
                    {'_id': midi['_id']},
                    {'$set': {
                        'md5': md5Value,
                        'Downloaded': True
                    }}
                )

            except:
                pass

            print('Progress: {:.2%}\n'.format(midi_collection.count({'Downloaded': True}) / midi_collection.count()))

        except:
            print(midi['Url'])


def download_jazz_midkar():
    import traceback

    midi_collection = get_midkar_jazz_collection()
    root_dir = 'E:/jazz_midkar/raw'
    socket.setdefaulttimeout(3)

    params = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'midkar.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://midkar.com/jazz/jazz_01.html'
    }

    cookies_dict = {
        'BX': 'eotmd2df96b5h&b=3&s=m6',
        'sc_is_visitor_unique': 'rx4375018.1586828808.2B1E41CF9BB14F4C4B3988AFC774B3DD.4.3.3.3.3.3.2.2.2'
    }
    cookies = requests.utils.cookiejar_from_dict(cookie_dict=cookies_dict, cookiejar=None, overwrite=True)

    session = requests.Session()
    requests.packages.urllib3.disable_warnings()
    session.headers.update(params)
    session.cookies = cookies

    for midi in midi_collection.find({'Downloaded': False}):
        name = midi['Name']
        url = midi['Url']
        source = midi['SourcePage']

        params = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'midkar.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': source
        }

        session.headers.update(params)

        try:

            save_path = root_dir + '/' + midi['md5'] + '.mid'

            with open(save_path, 'wb') as output:
                r = session.get(url, verify=False, timeout=5)
                output.write(r.content)

                if r.cookies.get_dict():
                    print(r.cookies.get_dict())
                    session.cookies = r.cookies
                if r.status_code != 200:
                    print('connection error ' + str(r.status_code))

            time.sleep(uniform(1, 2))
            print(os.path.getsize(save_path))

            try:
                pm = pretty_midi.PrettyMIDI(save_path)

                midi_collection.update_one(
                    {'_id': midi['_id']},
                    {'$set': {
                        'Downloaded': True
                    }}
                )
                print(
                    'Progress: {:.2%}\n'.format(midi_collection.count({'Downloaded': True}) / midi_collection.count()))

            except:
                print(midi['Url'])
                print(os.path.getsize(save_path))
                # print(traceback.format_exc())


        except Exception as e:
            print(midi['Url'])
            # print(traceback.format_exc())


def add_md5_to_all():
    midi_collection = get_jazz_midi_collection()
    m = hashlib.md5()
    for midi in midi_collection.find({'md5': {'$exists': False}}):
        name = midi['Name']
        m.update(bytes(name, 'utf-8'))
        md5Value = m.hexdigest()

        midi_collection.update_one(
            {'_id': midi['_id']},
            {'$set': {
                'md5': md5Value
            }}
        )


def find_not_properly_downloaded():

    midi_collection = get_midkar_jazz_collection()
    root_dir = 'E:/jazz_midkar/raw'
    for midi in midi_collection.find():
        path = root_dir + '/' + midi['md5'] + '.mid'
        # print(os.path.getsize(path))

        try:
            pm = pretty_midi.PrettyMIDI(path)
            mid = mido.MidiFile(path)

            if os.path.getsize(path) < 1000:
                print(f'{path} size 0')

        except:
            print(path)

            midi_collection.delete_one(
                {'_id': midi['_id']}
            )



if __name__ == '__main__':
    find_not_properly_downloaded()