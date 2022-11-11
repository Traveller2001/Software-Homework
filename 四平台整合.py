import time
from selenium import webdriver
import requests
import re
import uagent
import xlrd
import xlwt
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
import requests
from datetime import date
import json
from pyecharts.globals import ThemeType

flag = -1
domain = input("输入链接：")
if "https://www.bilibili.com" in domain:
    flag = 1
elif "https://www.icourse163.org" in domain:
    flag = 2
elif "https://coursehome.zhihuishu.com" in domain:
    flag = 3
elif "https://open.163.com/newview/movie/courseintro" in domain:
    flag = 4
elif "https://open.163.com/newview/movie/free?pid" in domain:
    flag = 5

if flag == 1: # B站

    import requests
    import bs4

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51"}

    resp = requests.get(url=domain, headers=header)
    page_content = resp.text

    obj = re.compile(r'<h1.*?class="video-title tit">(?P<name>.*?)</h1>', re.S)

    result = obj.finditer(page_content)
    for it in result:
        print(it.group("name"))


    def main():
        res = requests.get(url=domain, headers=header)
        res.encoding = res.apparent_encoding
        soups = bs4.BeautifulSoup(res.text, "html.parser")
        target = soups.find("meta", itemprop="thumbnailUrl")
        print(target["content"])


    if __name__ == '__main__':
        main()

elif flag == 2:  # 慕课
    domain = 'https://www.icourse163.org/course/NJUPT-1001639008'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    resp = requests.get(url=domain, headers=headers)
    obj = re.compile(r'.*?<div id="g-body">.*?<div id="j-courseImg" class="m-recimg">(?P<img>.*?)<div', re.S)
    obj_title = re.compile(r'<title>(?P<title>.*?)</title>', re.S)
    ret = obj.search(resp.text)
    ret_title = obj_title.search(resp.text)
    img_temp = ret.group('img')
    obj_temp = re.compile(r'<img.*?src="(?P<imgweb>.*?)".*?', re.S)
    ret_temp = obj_temp.search(img_temp)
    # 图片链接
    imgweb = ret_temp.group('imgweb')
    title = ret_title.group('title')
    print(imgweb, title)


elif flag == 3:  # 智慧树

    ua = uagent.get_ua()
    dic = {
        "User-Agent": "ua"
    }
    resp = requests.get(url=domain, headers=dic)
    page_content = resp.text

    obj = re.compile(
        r'<div class="course-img">.*?<img src="(?P<imgweb>.*?)".*id="selectedCourseName" >(?P<name>.*?)</div>', re.S)

    result = obj.finditer(page_content)
    for it in result:
        print(it.group("name"))
        print(it.group("imgweb"))

elif flag == 4:  # 网易公开课
    ua = uagent.get_ua()
    dic = {
        "User-Agent": "ua"
    }
    resp = requests.get(url=domain, headers=dic)
    page_content = resp.text

    obj = re.compile(
        r'<div class="content-left".*?<img src="(?P<photo>.*?)".*?</div>.*?<div class="content-title" .*?>(?P<name>.*?)</div>',
        re.S)

    result = obj.finditer(page_content)
    for it in result:
        print(it.group("photo"))
        print(it.group("name"))
elif flag == 5:  # 网易公开课2
    ua = uagent.get_ua()
    dic = {
        "User-Agent": "ua"
    }
    resp = requests.get(url=domain, headers=dic)
    page_content = resp.text

    obj = re.compile(r'<div class="video-title".*?>(?P<name>.*?)</div>', re.S)

    result = obj.finditer(page_content)
    for it in result:
        print(it.group("name"))



else:
    print("链接不合法！")
