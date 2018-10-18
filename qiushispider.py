

# //h2

#
# //i
import urllib.request
from lxml import etree
import json
url = 'https://www.qiushibaike.com/8hr/page/2/'
headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64;Trident/7.0;rv:11.0 )like Gecko'

}
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
html = response.read()
html = etree.HTML(html)
lists = html.xpath("//div[contains(@id,'qiushi_tag_')]")

dict={}
for list in lists:
    name = list.xpath(".//h2/text()")[0]
    img = list.xpath(".//img/@src")
    content = list.xpath(".//div[@class='content']/span/text()")
    haoxiao = list.xpath(".//i[0]/text()")
    comment = list.xpath(".//i[1]/text()")
    dict = {
        'name': name,
        'img': img,
        'content': content,
        'haoxiao': haoxiao,
        'comment': comment, }
    with open('duanzi.json', 'a', encoding='utr8') as f:
        f.write(json.dumps(dict, ensure_ascii=False))
