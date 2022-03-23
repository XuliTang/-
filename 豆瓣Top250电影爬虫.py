#coding=utf-8
import requests
from requests.exceptions import RequestException
import re
import json
import time
def get_one_page(url): #使用request.get()获取网页
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }  #构建headers，将爬虫程序发出的请求伪装成一个从浏览器发出的请求。伪装浏览器需要自定义请求报头，也就是在发送Request请求时，加入特定的Headers。
        response = requests.get(url, headers=headers)#使用request包的get方法，获取页面的响应报文
        if response.status_code == 200: #判断页面是否爬取成功
            return response.text # 返回页面的text文本信息
        return '页面无反应'
    except RequestException: #网络的各种变化可能会导致请求过程发生各种未知的错误导致程序中断，所以为了使我们的程序在请求时遇到错误，可以捕获这种错误，就要用到try…except方法
        return 'Request出现异常错误'


def parse_one_page(html):
    pattern = re.compile('<div.*?class="pic">.*?>(.*?)</em>.*?src="(.*?)".*?class="hd".*?'
                       'href="(.*?)".*?class="title">(.*?)</span>.*?class="bd">.*?导演: (.*?)&nbsp;&nbsp;&nbsp;'
                       '主演: (.*?)<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;'
                       '/&nbsp;(.*?)</p>', re.S)  #使用 compile 函数将正则表达式的字符串形式编译为一个 Pattern 对象
    items = re.findall(pattern, html) # findall对html页面进行正则匹配，查找所有满足条件的匹配文本，生成list格式[(XX,XX,XX,...),()]
    for item in items:#对items进行遍历
        yield {
            '电影排名': item[0],
            '电影图片链接': item[1],
            '电影详细内容链接': item[2],
            '电影名称': item[3].strip(),
            '导演': item[4].strip(),
            '主演': item[5].strip(),
            '上映日期': item[6].strip(),
            '国家': item[7].strip(),
            '类型':item[8].strip()
        }
        #yield是代替return的另一种方案:
        # 一般我们进行循环迭代的时候，都必须等待循环结束后才return结果。数量小的时候还行，但是如果循环次数上百万？上亿？我们要等多久？
        # 除了传统的多线程多进程外，我们还可以选择Generator生成器，也就是由yield代替return，每次循环都返回值，而不是全部循环完了才返回结果。


def write_to_file(content): #输出文件函数
    with open('/XXXX/result.txt', 'a', encoding='utf-8') as f: #输出文件路径 需要修改
        f.write(json.dumps(content, ensure_ascii=False) + '\n') #json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）



def main(offset):
    url = 'https://movie.douban.com/top250?start=' + str(offset) #抓取页面链接https://movie.douban.com/top250?start=0,25,75,100,125,150,175,200,225,250
    html = get_one_page(url) #抓取url对应的页面
    for item in parse_one_page(html): #通过parse_one_page(html)对url页面进行解析后，转换成为包含25项电影内容的生成器，对生成器进行循环
        print(item) #打印每一部电影的抓取内容，包括电影排名、电影图片链接、... 类型
        write_to_file(item) #调用输出文件函数

if __name__ == '__main__':
    for i in range(10): #翻页十次
       main(offset=i * 25) #循环依次输入https://movie.douban.com/top250?start=0,25,75,100,125,150,175,200,225,250
       time.sleep(4) #1s爬一次，防止被封





