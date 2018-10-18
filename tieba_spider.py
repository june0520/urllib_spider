from urllib import parse
import urllib .request
from lxml import etree

# class Spider(object):
#     def __init__(self):
#         self.page = 1
#         self.switch = True

def lode_page(url,filename):
    '''
    第二步，根据解析后的完整URL，发送请求。得到HTML，
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;Trident/7.0;rv:11.0 )like Gecko'很重要，之前的测试一直出现乱码。
    '''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;Trident/7.0;rv:11.0 )like Gecko'

    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf8')
    print('正在下载'+filename)
    lode_img(html)


def write_page(html, filename):
    with open(filename, 'w') as f:
        f.write(str(html))

    print('谢谢使用')


def tieba_url(kw,begin,endpage):
    '''
    第一步，根据用户输入的贴吧名，和页数，与基础URL进行拼街

    '''
    base_url = 'https://tieba.baidu.com/f?'
    data = {
        'kw': kw
    }
    baming = parse.urlencode(data)
    for page in range(begin, endpage+1):
        pn = (page-1)*50
        filename = '第'+str(page)+'页面'
        url = base_url + baming+"&pn="+str(pn)
        lode_page(url, filename)


def lode_img(html):
    '''
    第三步接收HTML，得到相关贴吧主页HTML，利用Xpath解析出每个帖子的链接，进入的相应帖子的主页，返回相应的HTML源码
    '''
    html = etree.HTML(html)
    results = html.xpath("//div[@class='threadlist_title pull_left j_th_tit ']/a/@href")
    for result in results:
        print('----------------------------------')
        full_url1 = 'https://tieba.baidu.com'+ str(result)
        response = urllib.request.urlopen(full_url1)
        html = response.read().decode('utf8')
        down_img(html)


def down_img(html):
    '''
    第四步得到个人主页的HTML，解析出源码中的图片的链接地址，再次发送request请求，并将结果写入到本地文件
    '''
    html = etree.HTML(html)
    results = html.xpath("//div//img[@class='BDE_Image']/@src")
    for result in results:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;Trident/7.0;rv:11.0 )like Gecko'

        }
        r = urllib.request.Request(result, headers=headers)
        response = urllib.request.urlopen(r)
        print('----------------------------------')
        r = response.read()
        name = result[-8:]
        with open(name, 'wb') as f:
            f.write(r)
    print('下载完成')


if __name__ == '__main__':
    # spider = Spider()
    kw = input('请输入您要查询的吧名：')
    begin = int(input('请输入起始页'))
    endpage = int(input('请输入终止页'))
    tieba_url(kw, begin, endpage)
