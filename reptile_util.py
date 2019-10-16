import requests
from lxml import etree
import sys
from PIL import Image
from io import BytesIO
import os


# 请求网页
class RequestHTML(object):

    # 浏览器请求头
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-User': '?1',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
              'Sec-Fetch-Site': 'cross-site',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9'}

    # 实例化时输入网址
    def __init__(self, base_url):
        # 目标网址
        self.__url = base_url
        # 用于存储Cookie
        self.__cookies = None
        # 保存图片时添加名称前缀，确保顺序
        self.__name_index = 1
        # 图片前缀补零使用
        self.__name_length = 5

    def set_url(self, url):
        self.__url = url

    # get方式请求网页
    def get_html(self, encoding=None):
        # get请求
        html = requests.get(self.__url, headers=self.header, cookies=self.__cookies)
        # 保存Cookie
        self.__cookies = html.cookies
        if encoding is not None:
            html.encoding = encoding
        return html

    # post方式请求网页
    def post_html(self, data=None, json=None, url=None):
        # post请求
        if url is None:
            html = requests.post(self.__url, data=data, json=json, headers=self.header, cookies=self.__cookies)
        else:
            html = requests.post(url, data=data, json=json, headers=self.header, cookies=self.__cookies)
        # 保存Cookie
        self.__cookies = html.cookies
        return html

    # 保存文件到本地
    def save_img(self, local_path, img_urls=None):
        # img_urls传递为list，用于批量保存图片
        if img_urls is not None:
            for img_url in img_urls:
                response = requests.get(img_url, headers=self.header, cookies=self.__cookies)
                img_name = os.path.split(img_url)[1]
                image = Image.open(BytesIO(response.content))
                index = str(self.__name_index)
                num = self.__name_length - len(index)
                if 0 > num:
                    num = self.__name_length - 1
                    self.__name_index = 1
                    index = 1
                self.__name_index = self.__name_index + 1
                image.save(os.path.join(local_path, '0' * num + index + '_' + img_name))
        else:
            # 调用时没有传图片url时，视为实例化时的base_url参数，用于保存一张图片
            response = self.get_html(self.__url)
            img_name = os.path.split(self.__url)[1]
            image = Image.open(BytesIO(response.content))
            image.save(os.path.join(local_path, img_name))


# 解析网页
class PathHTML(object):

    # 实例化时设置html文本与网页
    def __init__(self, html_text, base_url):
        # 请求网页的text文本
        self.__html = etree.HTML(html_text, base_url=base_url)
        # 请求网页的url（没搞明白什么用）
        self.__url = base_url

    # 通过xpath获取对应文本
    def get_documents(self, xpath):
        # 通过xpath定位要获取的节点或属性（谷歌安装个xpath插件很方便）
        documents = self.__html.xpath(xpath)
        return documents


# 根据url与xpath获取对应document
def main(url, xpath):
    requestHTML = RequestHTML(url)
    pathHTML = PathHTML(requestHTML.get_html().text, url)
    documents = pathHTML.get_documents(xpath)
    print(documents)


if __name__ == '__main__':
    args = sys.argv
    if 3 > len(args):
        print('请输入参数：1.url 2.xpath，如：')
        print(args[0], 'url', 'xpath')
    else:
        url = args[1]
        xpath = args[2]
        main(url, xpath)
        print('Done')


