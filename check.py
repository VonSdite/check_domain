import requests
import threadpool
import time
import re

import os
import sys
path = os.path.split(os.path.abspath(sys.argv[0]))[0]

from configobj import ConfigObj
# 从配置文件中读取
conf = ConfigObj(os.path.join(path, 'config.ini'), encoding='utf-8')
dic = conf['query']['dict']
base_domain = conf['query']['base_domain']
len_start = int(conf['query']['len_start'])
len_end = int(conf['query']['len_end'])

session = requests.Session()
session.headers.update({"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"})
url = "https://namebeta.com/api/query"
data = {
    'q': ''
}
pool = threadpool.ThreadPool(5)

label = {
    1: '未占用',
    2: '已被占用',
    3: '可能未被占用'
}

def get_client_id():
    while True:
        try:
            res = session.post(url='https://namebeta.com/api/token')
            text = res.json()[2]
            pattern1 = re.compile(r'/\*.*?\*/')
            pattern2 = re.compile(r'//.*?\n')
            pattern3 = re.compile(r"var .+ = ('.*'),")
            pattern4 = re.compile(r'(\[\[.*?\]\]);')
            text = pattern1.sub('', text)
            text = pattern2.sub('', text)
            x = pattern3.findall(text)[0]
            y = pattern4.findall(text)[0]
            x = eval(x)
            y = eval(y)
            for i, j in y:
                x = x[:i] + x[j:]
            break
        except Exception as e:
            print('[WARNING]', e)
            print('[WARNING LINE]', e.__traceback__.tb_lineno)
            pass

    return x

def get_domain(str, num):
        if(num == 1):
            for x in str:
                yield x
        else:
            for x in str:
                for y in get_domain(str, num-1):
                    yield x + y

def query(url, data, params):
    while True:
        try:
            res = session.post(url=url, data=data, params=params).json()
            print(data['q'], label[res[2][0][1]])
            if res[2][0][1] == 1 or res[2][0][1] == 3:
                with open(os.path.join(path, 'save.txt'), 'a', encoding='utf-8') as f:
                    f.write(data['q'] + ' ' + label[res[2][0][1]] + '\n')
            break
        except Exception as e:
            print('[WARNING]', e)
            print('[WARNING LINE]', e.__traceback__.tb_lineno)
            pass

if __name__ == '__main__':
    token = get_client_id()
    params = {'client_id': token}

    for x in range(len_start, len_end + 1):
        for s in get_domain(dic, x):
            data['q'] = s + base_domain
            pool.putRequest(
                threadpool.makeRequests(
                    query, 
                    [
                        (
                            (url, data, params), None
                        ),
                    ]
                )[0]
            )
    pool.wait()