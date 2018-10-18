import requests
from urllib.parse import urlencode
import os
import md5
from multiprocessing import Pool


def get_one_page(offset):
    params = {
        'offser': offset,
        'format': 'json ',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
          }
    url = 'https://www.toutiao.com/search/' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #以JSON的格式返回得到的源码
            return response.json()
    except requests.ConnectionError:
        return None


def get_img(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            imgs = item.get('img_list')
            #够成功一个生成器。将得到的图片的主题和链接返回
            for img in imgs:
                yield{
                    'title': title,
                    'img': img.get('url')
                    }

#接收返回的字典
def save_img(item):
    #创建文件夹
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        #请求这个图片的链接，获得图片的二进制数据，以二进制的方式写入相应主题的文件夹内，图片的名称使用其内容的Md5值，去重
        response = requests.get(item.get('img'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb')as f:
                    f.write(item.get(response.content))
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Faild to save image')


def main(offset):
    json = get_one_page(offset)
    for item in get_img(json):
        save_img(item)


GROUP_START = 1
GROUP_END = 20
if __name__ == '__main__':
    pool = Pool()
    #构建一个可迭代对象
    group = [x*20 for x in range(GROUP_START, GROUP_END +1)]
    pool.map(main, group)
    pool.close()
    pool.join()

    




