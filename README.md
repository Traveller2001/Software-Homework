# 一、PSP表格 

------------

| **PSP2.1**                              | **Personal Software Process Stages**    | 预计耗时 （分钟） | 实际耗时（分钟） |
| --------------------------------------- | --------------------------------------- | ----------------- | ---------------- |
| Planning                                | 计划                                    | 10                | 20               |
| · Estimate                              | · 估计这个任务需要多少时间              | 10                | 20               |
| Development                             | 开发                                    | 600               | 1365             |
| · Analysis                              | · 需求分析 (包括学习新技术)             | 300               | 900              |
| · Design Spec                           | · 生成设计文档                          | 10                | 20               |
| · Design Review                         | · 设计复审                              | 20                | 5                |
| · Coding Standard                       | · 代码规范 (为目前的开发制定合适的规范) | 10                | 10               |
| · Design                                | · 具体设计                              | 120               | 20               |
| · Coding                                | · 具体编码                              | 900               | 300              |
| · Code Review                           | · 代码复审                              | 180               | 10               |
| · Test                                  | · 测试（自我测试，修改代码，提交修改）  | 180               | 100              |
| Reporting                               | 报告                                    | 65                | 20               |
| · Test Repor                            | · 测试报告                              | 30                | 10               |
| · Size Measurement                      | · 计算工作量                            | 20                | 5                |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划          | 15                | 5                |
|                                         | · 合计                                  | 675               | 1405             |

# 二、任务要求的实现

----------

## 2.1 羡慕与技术栈

--------------

1.分析卫健委网站，进行分析

2.爬取目录的网址保存到excel里面

3.将excel里面的网址爬取文字

4.对爬取的文字进行分析，将需要的数据存入excel里面

5.制作数据可视化大屏

## 2.2 爬虫与数据处理

-----------

爬取一共42页目录里面的全部url，存入test.xlsx

> ```python
> url1 = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
> html = None
> 
> header = {
>     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
> }
> 
> while 1:
>     response = requests.get(url=url1, headers=header)
>     html = response.content.decode('UTf-8')
>     if response.status_code == 200:
>         print('success')
>         break
>     else:
>         time.sleep(1)
> soup = BeautifulSoup(html, 'html.parser')
> li = soup.find(class_ = 'list').find_all('li')
> 
> app1 = xw.App(visible=True, add_book=False)
> wb1 = app1.books.add()
> 
> listname = []
> listhref = []
> 
> for ii1 in li:
>     name = ii1.a['title']
>     href = 'http://www.nhc.gov.cn' + ii1.a['href']
>     listname.append(name)
>     listhref.append(href)
> 
> base_url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'
> add_url = '.shtml'
> for item in range(2,43):
>     while 1:
>         response=requests.get(url=base_url + str(item) + add_url , headers=header)
>         html = response.content.decode('UTF-8')
>         if response.status_code == 200:
>             print('success')
>             break
>         else:
>             time.sleep(1)
> 
>     soup = BeautifulSoup(html,'html.parser')
>     li = soup.find(class_ = 'list').find_all('li')
> 
>     for ii1 in li:
>         name = ii1.a['title']
>         href = 'http://www.nhc.gov.cn' + ii1.a['href']
>         listname.append(name)
>         listhref.append(href)
> 
> wb1.sheets['sheet1'].range('a1').options(transpose=True).value = listname
> wb1.sheets['sheet1'].range('b1').options(transpose=True).value = listhref
> 
> wb1.save(r'.\test.xlsx')
> wb1.close()
> app1.quit()
> ```

从test.xlsx里面取出url，爬取url里面的文字，对文字进行分析，将需要的数据存入test2.xlsx里面



> ```python
> provinces = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川',
>              '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海', '重庆', '兵团']
> HMT = ['香港特别行政区', '澳门特别行政区', '台湾地区']
> 
> app2 = xw.App(visible=True, add_book=False)
> wb2 = app2.books.add()
> sh2 = wb2.sheets['sheet1']
> 
> sh2.range('b1').value = '本土病例'
> sh2.range('c1:ah1').value = provinces
> sh2.range('ai1:ak1').value = HMT
> 
> wb1 = xw.Book('test.xlsx')
> sh1 = wb1.sheets['sheet1']
> 
> j = 1
> year = 0
> for k in range(782, 0, -1):
>     url = sh1.cells(k, 2).value
>     if '2020' in url:
>         year = 2020
>     if '2021' in url:
>         year = 2021
>     if '2022' in url:
>         year = 2022
>     while 1:
>         response = requests.get(url=url, headers=header)
>         html = response.content.decode('UTF-8')
>         if response.status_code == 200:
>             break
>         else:
>             time.sleep(1)
>     soup = BeautifulSoup(html, 'html.parser')
>     text = soup.find_all('p')
>     title = soup.find('title').text
>     data = []
>     data2 = []
>     if '肺炎疫情最新情况' in title:
>         j = j + 1
>         sh2.cells(j, 1).value = str(year) + '年' + title[title.find('至') + 1:title.find('日')+1]
>         print("success"+str(year) + '年' + title[title.find('至') + 1:title.find('日')+1])
>         for it in text:
>             detail = it.text
>             if '无本土病历' in detail:
>                 pass
>             elif '本土病例' in detail:
>                 i = detail.find('本土病例')+4
>                 sum1 = 0
>                 if detail[i] == '（':
>                     continue
>                 while detail[i] != '例':
>                     if '9' >= detail[i] >= '0':
>                         sum1 = sum1 * 10 + int(detail[i])
>                     i = i + 1
>                 data.append(sum1)
>                 i = detail.find('本土病例')
>                 while detail[i] != '（':
>                     i = i + 1
>                 st = ""
>                 while detail[i] != '）':
>                     st = st + detail[i]
>                     i = i + 1
>                 for n in provinces:
>                     if n in st:
>                         print(st.find(n)-1)
>                         if st[st.find(n)-1] == '在':
>                             sum1 = data[0]
>                         else:
>                             sum1 = 0
>                             ii = st.find(n)+len(n)
>                             while '9' >= st[ii] >= '0':
>                                 sum1 = sum1*10 + int(st[ii])
>                                 ii = ii + 1
>                         data.append(sum1)
>                     else:
>                         data.append(0)
>             for n in HMT:
>                 if n in detail:
>                     ii = detail.find(n)
>                     while detail[ii] != '区':
>                         ii = ii + 1
>                     ii = ii + 1
>                     sum1 = 0
>                     while '9' >= detail[ii] >= '0':
>                         sum1 = sum1*10 + int(detail[ii])
>                         ii = ii + 1
>                     data2.append(sum1)
>         if data:
>             pass
>         else:
>             data = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
>                     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
>         print(data)
>         print(data2)
>         rng = sh2[j-1, 1]
>         sh2.range(rng).value = data
>         rng = sh2[j-1, 34]
>         sh2.range(rng).value = data2
> ```

现在我需要的数据都在test2.xlsx里面了。我使用pyecharts来对数据进行可视化。

> ```python
> wb2.save(r'.\test2.xlsx')
> wb2.close()
> app2.quit()
> wb = xw.Book('test2.xlsx')
> sh = wb.sheets['sheet1']
> usedrange = sh.used_range
> lastrow = usedrange.last_cell.row
> value = []
> ku = ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa',
>     'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak']
> for r in ku:
>     rng = sh.range(r + str(lastrow))
>     value.append(sh.range(rng).value)
> rng = sh.range('a' + str(lastrow))
> title = sh.range(rng).value
> attr = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
>     '湖南', '广东', '海南', '四川',
>     '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京', '天津', '上海',
>     '重庆', '兵团', '香港', '澳门', '台湾']
> c = (
>     Map()
>     .add("新增数量", [list(z) for z in zip(attr, value)], "china", )
>     .set_global_opts(
>         title_opts=opts.TitleOpts(title=title + "新冠疫情日新增", subtitle="数据来源——卫健委"),
>         visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True), )
>     .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
>     .render("疫情地图.html")
> )
> ```

## 2.3 数据统计接口部分的性能改进

------------

爬取卫健委网站占了整个程序最长的时长，耗时约60-80min。约60-80min完成整个程序。

## 2.4 每日热点的实现思路

-------------

对过去十四天未出现疫情而今天突然出现疫情的城市设为热点

对之前有疫情，但满十四天未出现新增的城市设为热点

## 2.5 数据可视化界面的展示

-------------

![](https://s3.bmp.ovh/imgs/2022/09/20/a9b9690ea6fe2bd8.png)

# 三、心得体会

---------

- 学习了python的知识，掌握了一项新工具
- 在实践中学会运用各种库

