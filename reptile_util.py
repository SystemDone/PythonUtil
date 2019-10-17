import requests
from lxml import etree
from PIL import Image
from io import BytesIO
import os
from fake_useragent import UserAgent


# 请求网页
class RequestHTML(object):

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

    # 重置URL
    def set_url(self, url):
        self.__url = url

    # get方式请求网页
    def get_request(self, params=None, headers=None, encoding='UTF-8'):
        # 添加请求头
        if headers is None:
            headers = self.get_radom_headers()
        # get请求
        request = requests.get(self.__url, params=params, headers=headers, cookies=self.__cookies)
        # 保存Cookie
        self.__cookies = request.cookies
        # 设置编码
        request.encoding = encoding
        return request

    # post方式请求网页
    def post_request(self, data=None, json=None, headers=None, encoding='UTF-8'):
        # 添加请求头
        if headers is None:
            headers = self.get_radom_headers()
        # post请求
        request = requests.post(self.__url, data=data, json=json, headers=headers, cookies=self.__cookies)
        # 保存Cookie
        self.__cookies = request.cookies
        # 设置编码
        request.encoding = encoding
        return request

    # 保存一张图片到本地
    def save_img(self, local_path):
        request = self.get_request()
        img_name = os.path.split(self.__url)[1]
        image = Image.open(BytesIO(request.content))
        image.save(os.path.join(local_path, img_name))
        print('保存完成')

    # 保存文件到本地
    def save_img_batch(self, local_path, img_urls):
        for img_url in img_urls:
            self.set_url(img_url)
            request = self.get_request()
            img_name = os.path.split(img_url)[1]
            image = Image.open(BytesIO(request.content))
            index = str(self.__name_index)
            num = self.__name_length - len(index)
            if 0 > num:
                num = self.__name_length - 1
                self.__name_index = 1
                index = 1
            self.__name_index = self.__name_index + 1
            image.save(os.path.join(local_path, '0' * num + index + '_' + img_name))
        print('保存完成')

    # 随机生成请求头
    def get_radom_headers(self):
        return {'User-Agent': UserAgent().random}


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
