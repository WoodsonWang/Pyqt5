"""
@author:Wang Xinsheng
@File:getmusic.py
@description:...
@time:2020-10-25 20:49
"""

import requests
import os
import json
import ast

# url = 'http://gequdaquan.net/gqss/api.php'
url = 'https://api.zhuolin.wang/api.php'
# https://api.zhuolin.wang/api.php?types=url&id=418aa3f6c40e46f847fa79ae85b16656&source=kugou
download_url = 'http://fs.ios.kugou.com/202010252247/9cb1b4c09c2c373b6263ab79a7355d13/G221/M04/0A/00/HQ4DAF8ecg6AV-2FACv-Nh0P7z4142.mp3'

def req_get(music_name,source,baseurl=url):
    '''
    获取歌曲列表
    :param music_name:
    :param source: 数字
    :param baseurl:
    :return:
    '''
    '0 网易云  1  QQ  2 虾米  3 酷狗 4 百度'
    sources = ['netease','tencent','xiami','kugou','baidu']
    getdata = {
        # "callback ": 'jQuery1113023236435553523216_1603633972378',
        'types': 'search',
        'count': 20,
        'source': sources[source],
        'pages': 1,
        'name': music_name
    }
    r = requests.get(baseurl,params=getdata)
    result = r.content.decode('unicode-escape')
    return result

def get_download_url(id,source):
    baseurl = 'https://api.zhuolin.wang/api.php'
    getdata = {
        'types':'url',
        'id':id,
        'source':source
    }
    get = requests.get(baseurl, params=getdata)
    print(get.url)
    print(get.text)
    # {
    #     "url": "http:\/\/fs.ios.kugou.com\/202010270000\/cf99f8ea3eb72ce34255cb3c7fbe75e2\/G206\/M05\/09\/13\/bocBAF5UBWqAa07SADqfOLPG3ig468.mp3",
    #     "size": 3841848, "br": 128}


    result = ast.literal_eval(get.text)
    # {
    #     "url": "http:\/\/fs.ios.kugou.com\/202010261127\/f0ecb08e34443b411298eba028163f6d\/G221\/M04\/0A\/00\/HQ4DAF8ecg6AV-2FACv-Nh0P7z4142.mp3",
    #     "size": 2883126, "br": 128}
    download_url = result['url'].replace('\\','')
    music_size = result['size']
    return download_url,music_size


def download_file(base_path,file_url,music_size,name,download_signal):
    '''下载文件'''
    base_path = base_path.replace('/','\\')
    file_url = file_url.replace('\\','')
    print(file_url)
    res = requests.get(file_url, stream=True)
    # path = 'D:\codeproject\python\Pachong\Music\data'
    file_path = os.path.join(base_path, name)

    print(file_path)
    with open(file_path,'wb') as f:
        step = 100 / (music_size / 1024)
        progress = 0
        for chunk in res.iter_content(chunk_size=1024):
            progress += step
            download_signal.emit(progress)
            f.write(chunk)

    print('{}成功下载'.format(name))


postdata = {
    "callback ": 'jQuery1113023236435553523216_1603633972378',
    'types':'search',
    'count':100,
    'source':'tencent', # tencent  kugou
    'pages':1,
    'name':'红玫瑰'
}

class Music:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,id):
        self.__id = id

    @property
    def artist(self):
        return self.__artist
    @artist.setter
    def artist(self,artist):
        self.__artist = artist

    # 下载源
    @property
    def source(self):
        return self.__source
    @source.setter
    def source(self,source):
        self.__source = source





# r = requests.post(url,data=postdata)
# # 将\u unicode编码的字符串正常显示为中文
# result = r.content.decode('unicode-escape')
if __name__ == '__main__':
    # music_list = []
    result = req_get('忘川彼岸',2,)
    print(result)
    # load = ast.literal_eval(result)
    # for item in load:
    #     print(item)
    #     music = Music()
    #     music.name = item['name']
    #     music.id = item['id']
    #     music.artist = item['artist']
    #     music.source = item['source']
    #     music_list.append(music)
    # for m in music_list:
    #     print(m.name)
    # download_file('http:\/\/fs.ios.kugou.com\/202010252254\/a10ab1cae0e3b6c036a436848d07b2a0\/G221\/M04\/0A\/00\/HQ4DAF8ecg6AV-2FACv-Nh0P7z4142.mp3',"忘川彼岸.mp3")
    # get_download_url('33e1cefb0164f8eb0a4f30ce51336ed4','kugou')