> Github链接：[Exungsh/032002337: An Covid-19 data analysis program based on the Health Commission(NHC) announcement](https://github.com/Exungsh/032002337)

# 一、PSP表格

| Personal Software Process Stages                             | 预估耗时（分钟） | 实际耗时（分钟） |
| :----------------------------------------------------------- | :--------------: | :--------------: |
| Planning（计划）                                             |        60        |        60        |
| Estimate（估计时间）                                         |        20        |        10        |
| Development（开发）                                          |       600        |       900        |
| Analysis（需求分析（包括学习新技术））                       |       300        |       360        |
| Design Spec（生成设计文档）                                  |        30        |        20        |
| Design Review（设计复审）                                    |        0         |        0         |
| Coding Standard（代码规范 ）                                 |        0         |        0         |
| Design（具体设计）                                           |        0         |        0         |
| Coding（具体编码）                                           |       600        |       900        |
| Code Review（代码复审）                                      |       300        |       180        |
| Test（测试（自我测试，修改代码，提交修改））                 |       120        |       180        |
| Test Report（测试报告）                                      |        0         |        0         |
| Size Measurement（计算工作量）                               |        0         |        0         |
| Postmortem & Process Improvement Plan（事后总结, 并提出过程改进计划） |        0         |        0         |
| Total（合计）                                                |       2030       |       2610       |

其实不是特别能领会到做这个表的意义，知道整个流程很重要，但是这个预估时间和实际时间的意义emmm，其实真正coding的时候很多项工作都是同时进行的，很难进行量化，而且也不会特地去计时。

<br>

---

<br>

# 二、任务要求的实现

### 1、项目设计与技术栈

#### 1.1、项目设计

整个项目主要分为三大块

1. 爬取卫健委疫情通报的网址（value）和相应的日期（key）形成字典，存入json文件
2. 通过遍历字典，爬取历史通报内容，生成txt文件
3. 通过与用户交互（指定日期），分析指定txt文件，生成表格、柱状图和地图

#### 1.2、技术栈

1. Python
2. Html + CSS （Beautifulsoup）
3. 深度学习（指我学习通报格式）
<br>
---
<br>

### 2、爬虫与数据处理

业务主要分为三块

> 1. get_url.py：获取网址列表
> 2. get_text.py：获取通告内容
> 3. get_result.py：用户交互，获取最后结果
>
> get_url.py --> url_list.json --> get_text.py --> txt --> get_result.py --> 表格、柱状图、地图

#### 2.1、get_url.py

**核心代码：**

```python
area = requests.get(target_url, headers=headers).text  # 爬取网页文字
    bs = BeautifulSoup(area, "html.parser")
    # 获取a标签（目的是获取通告网址）
    a_url = bs.select('.list > ul > li > a')
    # 获取span标签（目的是获取日期）
    span_date = bs.select('.list > ul > li > span')
    for a in a_url:
        url.append('http://www.nhc.gov.cn/' + a['href'])
    for span in span_date:
        date.append(span.text)
    # 打包成字典
    result = dict(zip(date, url))
    return result
```

遍历每页可获得一个**{date:url}字典**

```python
with open("url_list.json", "w") as f:
    f.write(json.dumps(url_dict, indent=4))
```

导出为**json**文件

json文件内容（部分）：

```json
{
    "2022-09-12": "http://www.nhc.gov.cn//xcs/yqtb/202209/093a5fe2183b42169296326741d81565.shtml",
    "2022-09-11": "http://www.nhc.gov.cn//xcs/yqtb/202209/338e611615da4998a1202694eee8f196.shtml",
    "2022-09-10": "http://www.nhc.gov.cn//xcs/yqtb/202209/8ac84d72227c4a318694ddae45412c9a.shtml",
    "2022-09-09": "http://www.nhc.gov.cn//xcs/yqtb/202209/0702822269e648a882c267aa672cebf8.shtml",
    "2022-09-08": "http://www.nhc.gov.cn//xcs/yqtb/202209/78ea88c5c23e41c391376ee9b103cfec.shtml",
    "2022-09-07": "http://www.nhc.gov.cn//xcs/yqtb/202209/b9867ea1be624141b41f461a431239d7.shtml",
    "2022-09-06": "http://www.nhc.gov.cn//xcs/yqtb/202209/892ec8bb4db44a96bd06169ac2d7de09.shtml",
    "2022-09-05": "http://www.nhc.gov.cn//xcs/yqtb/202209/9a6ef43336a2401ca6dc4f2e6f97e5a6.shtml",
    "2022-09-04": "http://www.nhc.gov.cn//xcs/yqtb/202209/cb9e0c28d4b2467fac0ca2871bbfd95b.shtml",
    "2022-09-03": "http://www.nhc.gov.cn//xcs/yqtb/202209/97243736d6e94317810ac51ba23fe189.shtml",
    "2022-09-02": "http://www.nhc.gov.cn//xcs/yqtb/202209/e0a18445e0ab47608527b9c910f77699.shtml",
    "2022-09-01": "http://www.nhc.gov.cn//xcs/yqtb/202209/b236ae4939f24155a506f0cfb0f16ace.shtml",
    "2022-08-31": "http://www.nhc.gov.cn//xcs/yqtb/202208/8fbbe614bd0c4a5ca9cf8a9e4c289e9a.shtml",
    "2022-08-30": "http://www.nhc.gov.cn//xcs/yqtb/202208/2cc3c1a07dd348b09afac2a880ca72ca.shtml"
}
```



---

#### 2.2、get_text.py

**核心代码：**

获取通告内容函数：

```python
# 传入网址，返回网页内所有p标签内容
def get(target_url):
    area = requests.get(target_url, headers=headers).text  # 爬取网页文字
    bs = BeautifulSoup(area, "html.parser")
    d = bs.findAll('p')  # d存储所有p标签中的内容
    return d
```

对返回的列表进行合并处理，获得完整的一段话

```python
for p in p_data:
    data = data + p.text
fh = open(date+'.txt', 'w', encoding='utf-8')
fh.write(data)
fh.close()
```

txt中内容：

```
9月8日0—24时，31个省（自治区、直辖市）和新疆生产建设兵团报告新增确诊病例301例。其中境外输入病例42例（广东16例，福建9例，上海6例，北京4例，云南2例，天津1例，辽宁1例，黑龙江1例，山东1例，陕西1例），含2例由无症状感染者转为确诊病例（山东1例，广东1例）；本土病例259例（四川59例，内蒙古42例，广东36例，广西22例，西藏20例，北京17例，山东16例，黑龙江13例，青海7例，贵州6例，陕西4例，辽宁3例，江苏3例，云南3例，新疆3例，天津1例，江西1例，河南1例，海南1例，重庆1例），含41例由无症状感染者转为确诊病例（内蒙古15例，黑龙江7例，四川4例，广东3例，新疆3例，西藏2例，辽宁1例，山东1例，河南1例，重庆1例，贵州1例，陕西1例，青海1例）。无新增死亡病例。无新增疑似病例。当日新增治愈出院病例336例，其中境外输入病例30例，本土病例306例（海南88例，四川71例，西藏30例，黑龙江24例，陕西20例，重庆17例，广东14例，青海14例，河南5例，新疆4例，内蒙古3例，山西2例，辽宁2例，浙江2例，福建2例，山东2例，湖北2例，云南2例，天津1例，湖南1例），解除医学观察的密切接触者32566人，重症病例较前一日减少10例。境外输入现有确诊病例560例（无重症病例），无现有疑似病例。累计确诊病例22906例，累计治愈出院病例22346例，无死亡病例。截至9月8日24时，据31个省（自治区、直辖市）和新疆生产建设兵团报告，现有确诊病例6226例（其中重症病例28例），累计治愈出院病例234876例，累计死亡病例5226例，累计报告确诊病例246328例，无现有疑似病例。累计追踪到密切接触者5632275人，尚在医学观察的密切接触者278389人。31个省（自治区、直辖市）和新疆生产建设兵团报告新增无症状感染者1103例，其中境外输入70例，本土1033例（西藏347例，黑龙江109例，山东81例，内蒙古77例，辽宁77例，广西77例，四川71例，江西56例，广东28例，新疆27例，青海15例，贵州13例，湖北12例，陕西11例，河南8例，海南5例，天津4例，福建3例，甘肃3例，北京2例，吉林2例，上海2例，云南2例，江苏1例）。当日解除医学观察的无症状感染者1710例，其中境外输入109例，本土1601例（西藏902例，青海155例，海南135例，陕西59例，新疆50例，河北49例，河南38例，黑龙江34例，湖北34例，山东28例，四川27例，江西14例，重庆13例，甘肃12例，广西11例，辽宁8例，上海6例，广东5例，江苏4例，湖南4例，内蒙古3例，山西2例，浙江2例，安徽2例，云南2例，天津1例，吉林1例）；当日转为确诊病例43例（境外输入2例）；尚在医学观察的无症状感染者24048例（境外输入648例）。累计收到港澳台地区通报确诊病例5977507例。其中，香港特别行政区396687例（出院77564例，死亡9769例），澳门特别行政区793例（出院787例，死亡6例），台湾地区5580027例（出院13742例，死亡10170例）。
（注：媒体引用时，请标注“信息来自国家卫生健康委员会官方网站”。） 地址：北京市西城区西直门外南路1号  邮编：100044  电话：010-68792114  ICP备案编号：京ICP备18052910号  京公网安备 11010202000005号中华人民共和国国家卫生健康委员会  版权所有  技术支持：国家卫生健康委员会统计信息中心  网站标识码：bm24000006
```

---

#### 2.3、get_result.py

**核心代码：**

使用**re库**找到需要的文字段

使用**jieba库**对中文文本进行切词，将切词结果转化为列表

```python
new_text = re.findall('本土病例.*?）', text)[0]
print(new_text)
cut = jieba.cut(new_text, cut_all=False)  # jieba切词
new_result = ' '.join(cut)
new_result = new_result.split()
print(new_result)
```

得出结果：

```
['本土', '病例', '259', '例', '（', '四川', '59', '例', '，', '内蒙古', '42', '例', '，', '广东', '36', '例', '，', '广西', '22', '例', '，', '西藏', '20', '例', '，', '北京', '17', '例', '，', '山东', '16', '例', '，', '黑龙江', '13', '例', '，', '青海', '7', '例', '，', '贵州', '6', '例', '，', '陕西', '4', '例', '，', '辽宁', '3', '例', '，', '江苏', '3', '例', '，', '云南', '3', '例', '，', '新疆', '3', '例', '，', '天津', '1', '例', '，', '江西', '1', '例', '，', '河南', '1', '例', '，', '海南', '1', '例', '，', '重庆', '1', '例', '）']
```

对列表进行处理，得出最终需要的数据，同时写入excel表格

```python
count = 0 # 记录现在遍历到列表第几个元素了

# 写excel标题
title = ['省份', '新增确诊']
col = 0
for i in title:
    sheet.write(0, col, i)
    col += 1
new_row = 1

# 开始处理列表
for word in new_result:
    if word.isdigit():
        if new_result[count - 2] == '本土':
            new_sum = int(word) # new_sum存储总人数
        else:
            new_num.append(int(word)) # 将人数添加到new_num列表中
            new_prov.append(new_result[count - 1]) # 将省份添加到new_prov列表中
            sheet.write(new_row, 0, new_result[count - 1]) # 写入表格
            sheet.write(new_row, 1, int(word)) #写入表格
            new_row += 1
    count += 1
```
<br>

---

<br>

### 3、数据统计接口部分的性能改进
用python的cprofiler库对**get_result.py**进行分析，得出结果如下：

```python
214 function calls (207 primitive calls) in 0.001 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.001    0.001 <string>:1(<module>)
        2    0.000    0.000    0.000    0.000 enum.py:358(__call__)
        2    0.000    0.000    0.000    0.000 enum.py:670(__new__)
        1    0.000    0.000    0.000    0.000 enum.py:977(__and__)
        1    0.000    0.000    0.001    0.001 re.py:250(compile)
        1    0.000    0.000    0.001    0.001 re.py:289(_compile)
        1    0.000    0.000    0.000    0.000 sre_compile.py:249(_compile_charset)
        1    0.000    0.000    0.000    0.000 sre_compile.py:276(_optimize_charset)
        2    0.000    0.000    0.000    0.000 sre_compile.py:453(_get_iscased)
        1    0.000    0.000    0.000    0.000 sre_compile.py:461(_get_literal_prefix)
        1    0.000    0.000    0.000    0.000 sre_compile.py:492(_get_charset_prefix)
        1    0.000    0.000    0.000    0.000 sre_compile.py:536(_compile_info)
        2    0.000    0.000    0.000    0.000 sre_compile.py:595(isstring)
        1    0.000    0.000    0.000    0.000 sre_compile.py:598(_code)
      3/1    0.000    0.000    0.000    0.000 sre_compile.py:71(_compile)
        1    0.000    0.000    0.001    0.001 sre_compile.py:759(compile)
        3    0.000    0.000    0.000    0.000 sre_parse.py:111(__init__)
        7    0.000    0.000    0.000    0.000 sre_parse.py:160(__len__)
       18    0.000    0.000    0.000    0.000 sre_parse.py:164(__getitem__)
        7    0.001    0.000    0.001    0.000 sre_parse.py:172(append)
      3/1    0.000    0.000    0.000    0.000 sre_parse.py:174(getwidth)
        1    0.000    0.000    0.000    0.000 sre_parse.py:224(__init__)
        8    0.000    0.000    0.000    0.000 sre_parse.py:233(__next)
        2    0.000    0.000    0.000    0.000 sre_parse.py:249(match)
        6    0.000    0.000    0.000    0.000 sre_parse.py:254(get)
        1    0.000    0.000    0.000    0.000 sre_parse.py:286(tell)
        1    0.000    0.000    0.001    0.001 sre_parse.py:435(_parse_sub)
        2    0.000    0.000    0.001    0.000 sre_parse.py:493(_parse)
        1    0.000    0.000    0.000    0.000 sre_parse.py:76(__init__)
        2    0.000    0.000    0.000    0.000 sre_parse.py:81(groups)
        1    0.000    0.000    0.000    0.000 sre_parse.py:923(fix_flags)
        1    0.000    0.000    0.001    0.001 sre_parse.py:939(parse)
        1    0.000    0.000    0.000    0.000 {built-in method _sre.compile}
        1    0.000    0.000    0.001    0.001 {built-in method builtins.exec}
       25    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
    29/26    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.max}
        9    0.000    0.000    0.000    0.000 {built-in method builtins.min}
        6    0.000    0.000    0.000    0.000 {built-in method builtins.ord}
       48    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        5    0.000    0.000    0.000    0.000 {method 'find' of 'bytearray' objects}
        1    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
```

* 可以看出最后和用户交互的程序性能还是很不错的，响应时间很快。
* 至于另外两个程序get_url.py和get_text.py，为了保证能把数据爬下来，代码中有大量的循环、sleep，故性能较差。

<br>

---

<br>

### 4、每日热点的实现思路

柯老板提过可以做七日内疫区统计，自己主要的思路如下：

* 因为要做七日统计，所以原本的get_result.py程序已经不能满足要求。
* 但是可以利用get_result.py程序，将分析结果整理为字典存入json。
* 在程序中对所有日期进行遍历即可得到一个有着每天新增与无症状人数的json文件。
* 用户输入日期，对日期前七天的数据进行查询合并（set），打印出所有有新增的省份。

<br>

---
<br>

### 5、数据可视化界面的展示

* 可视化界面做了**地图**和**柱状图**两个版本
* 使用pyecharts库进行可视化
* 传入数据为四个字典：**新增确诊省份**、**新增确诊人数**、**新增无症状省份**、**新增无症状人数**

**核心代码：**

**柱状图：**

```python
bar_new = (
    Bar()
    .add_xaxis(new_prov)# x轴为省份名
    .add_yaxis("新增确诊人数", new_num)# y轴为人数
    .set_global_opts(title_opts=opts.TitleOpts(
        title=input_date+"全国新增确诊和无症状人数汇总",
        subtitle='全国共新增确诊' +str(new_sum)+ "人，新增无症状"+str(wzz_sum)+'人'),
        legend_opts=opts.LegendOpts(pos_top="8%")
    )
)
bar_wzz = (
    Bar()
    .add_xaxis(wzz_prov)
    .add_yaxis("新增无症状人数", wzz_num)
    .set_global_opts(legend_opts=opts.LegendOpts(pos_bottom="40%"))
)
# 将两张表组合展示
(Grid(init_opts=opts.InitOpts(width='1500px', height='600px'))
 .add(bar_new, grid_opts=opts.GridOpts(pos_top="90px", pos_bottom="60%", height="200px"))
 .add(bar_wzz, grid_opts=opts.GridOpts(pos_top="60%", height="200px"))
 ).render(input_date+'全国新增确诊和无症状人数柱状图.html')
```

**结果：**

![image](https://img2022.cnblogs.com/blog/2288880/202209/2288880-20220916154106875-457939111.png)


**地图：**

```python
# 地图
x = []  # 把各省感染人数与各省对应
for z in zip(list(new_prov), list(new_num)):
    list(z)
    x.append(z)
area_map = Map()
area_map.add("中国疫情新增确诊分布图", x, "china", is_map_symbol_show=False)
area_map.set_global_opts(title_opts=opts.TitleOpts(title="中国疫情新增确诊人数分布地图", subtitle=date),
                         visualmap_opts=opts.VisualMapOpts(
                             is_piecewise=True,
                             pieces=[
                                 {"min": 1500, "label": '>10000人', "color": "black"},
                                 {"min": 500, "max": 15000, "label": '500-1000人', "color": "#6F171F"},
                                 {"min": 100, "max": 499, "label": '100-499人', "color": "#C92C34"},
                                 {"min": 10, "max": 99, "label": '10-99人', "color": "#E35B52"},
                                 {"min": 1, "max": 9, "label": '1-9人', "color": "#F39E86"}]))
area_map.render(input_date + '全国新增确诊地图.html')
```

**结果：**

![image](https://img2022.cnblogs.com/blog/2288880/202209/2288880-20220916154114074-1334948674.png)

<br>

---

<br>


# 三、心得体会

* 一开始以为只是去任意网页爬取疫情数据（其实是不愿意面对卫健委的文本数据），直接去爬下网易的json文件，分析做表一套带走。
* 后面确认了一定要爬卫健委很痛苦，刚开始测试爬取的时候发现卫健委反爬机制有、烦，要么返回的是乱码的网页，要么干脆412什么都爬不到（后面发现只要不是爬的特别猛不会碰到这种情况），解决方案是换新的cookie或者反复爬取直到出现有意义结果。
* 所以最最基本的问题是，我怎么判断我爬的东西是乱码，还是我想要的数据。解决方案是用beautifulsoup获取网页文本，如果返回的列表是空的，说明是乱码，重新爬取。
* 鉴于爬取失败率高所以将这个大任务分为三个程序，避免放在一个程序里一个错误满盘皆输。
* 对文本分析那一块，得狠狠吐槽卫健委网页的格式，近期的通告每一段独享一个p标签，所以我很想当然地用beautifulsoup获取所有p标签内容，通过下标来区分第几段，后面进行随机测试的时候发现几个月前的通告所有的正文是放在同一个p标签下面的，直接从根本逻辑上杀死比赛，只能重新写（也说明测试很重要）
* 第二版程序的逻辑干脆就不分段了，直接把所有文字搞成一坨，正则切分完事。
* 要非常感谢的是jieba库，这是我大一上python选修的时候老师教的一个库，能根据中文语义对文本进行切词，为我省下了不少工作。
* 最后出来的程序并不是特别完美，越久的通告格式就越不统一，数据越容易出现缺失。毕竟是通过正则进行查询，也是意料之内，告诉了我们事情堆太多就做不完了，只有实时更新算法，日日精进才能游刃有余（胡言乱语）
* 当然python确实好玩，累得要死但是好玩。
* 最后的最后，这次作业好多啊！