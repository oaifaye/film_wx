'''
Created on 2017年12月15日

@author: Administrator
'''
import urllib.request
import lxml.html

class HttpUtil():
    headers = {'User-Agnet': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36', 'Connection': 'keep-alive'}
    '''从网页地址获取到html'''
    def getHtmlFromUrl(self,url,encode):
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode(encode)
        return html
    
    '''从网址获取xml的doc'''
    def getLxmlDocFromUrl(self,url,encode):
        html= self.getHtmlFromUrl(url, encode)
        doc = lxml.html.fromstring(html)
        return doc