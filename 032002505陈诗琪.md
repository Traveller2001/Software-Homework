**我的项目github链接：https://github.com/csq200505/032002505**


# 一、PSP表格
| PSP2.1                                      | Personal Software<br/>Process Stages | 预估耗时<br/>（分钟） | 实际耗时<br/>（分钟） |
|---------------------------------------------|--------------------------------------|---------------|---------------|
| Planning                                    | 计划                                   | 30            | 90            |
| · Estimate                                  | · 估计这个任务需要多少时间                       | 30            | 90            |
| Development                                 | 开发                                   | 2520          | 3840          |
| · Analysis                                  | · 需求分析                               | 30            | 60            |
| · Design Spec                               | · 生成设计文档                             | 30            | 0             |
| · Design Review                             | · 设计复审                               | 20            | 40            |
| · Coding Standard                           | · 代码规范                               | 10            | 30            |
| · Design                                    | · 具体设计                               | 60            | 60            |
| · Coding                                    | · 具体编码                               | 1950          | 2990          |
| · Code Review                               | · 代码复审                               | 60            | 180           |
| · Test                                      | · 测试                                 | 360           | 480           |
| Reporting                                   | 报告                                   | 70            | 160           |
| · Test Repor                                | · 测试报告                               | 20            | 0             |
| · Size Measurement                          | · 计算工作量                              | 20            | 10            |
| · Postmortem & Process<br/>Improvement Plan | · 事后总结                               | 30            | 150           |
|                                             | ·合计                                  | 2620          | 4090          |

# 二、任务要求的实现

## 2.1 项目设计与技术栈

在理解完这个题目之后，我认为这个项目非常有复杂。包容万象，囊括了许多技术。这次的任务我拆分为以下部分进行设计与实现：

* 爬虫设计和数据获取：通过Java的爬虫工具Jsoup实现
* 数据解析和录入：通过Java正则表达式进行匹配，并录入数据库
* Excel表格生成：通过从数据库中获取数据并生成表格存于内存中
* 数据大屏实现：通过React+ant design charts实现大屏
* 每日热点算法实现

其中，每日热点算法因为时间关系被迫放弃，其他几个部分均已完成。

技术栈如下：

* 语言- Java（主要）, JavaScript， TypeScript， css， html（数据大屏）
* 框架- Spring Boot（服务端）， React（数据大屏）
* 数据库- MySQL， 包括ORM框架Mybatis和Mybatis-plus
* 爬虫- Jsoup
* Excel导出 - EasyExcel

## 2.2 爬虫与数据处理

### 爬虫

通过设计，这个项目可以实现数据的持久度 —— 不仅能够完备的获得以前的数据，只要程序保持运行，新的数据就会源源不断的加入。（自动不断请求，总会成功吧）

```
-spider
  |_ CovidDataSpider.java
  |_ DataHandler.java
  |_ HttpHeaderConsts.java
```

以上是爬虫的核心代码类，数据库模型类则如下：

```
- entity
	|_ AccessURL.java
	|_ DailyArticle.java
	|_ DailyProvincialData.java
	|_ DailyTotalData.java
	|_ FailedURL.java
	|_ SpiderRecord.java
```

由于卫健委的网站具有相当强大的反爬虫功能，请求经常会被412，我想了很多办法，包括使用代理IP池（免费的），修改请求头user-agent等等，都没有很大的作用。最后只能靠提高访问频率不断尝试，才能最终成功。同时，我发现卫健委的疫情数据的分页网址是有规律可循的，可以通过遍历不断尝试获取，但里面的具体通报网页则没有规律，必须爬取之后再批量访问。因此，我设计了SpiderRecord表和FailedURL表和AccessURL表，并将爬取过程切割为两级：

*1*. 通过遍历40+目录页获取所有具体通报对应的网页URL，一共约978条（首次爬取时）

*2*. 通过遍历978条记录，将通报内容和发布时间获取并入库。

AccessURL记录这978条URL，每次爬虫访问的成功率都会被记录在SpiderRecord中而每次爬虫失败的网址都会被记录在FailedURL表里，在每一次爬取结束后，都会对按时间倒序获取对应等级下爬取失败的内容，不断的重新尝试，直到全部爬取成功为止。

最后，经历了两天多的不断尝试爬取，终于爬取到了全部的网页内容到daily_Article表中，并开始准备处理数据。但我发现daily_article中的数据相较access_url，**有着5条的数据缺失**。经核查，我发现由于我将数据库主键设置为通报发布时间，而这几条有缺失数据的日期均有多于一篇的新通报发出（多余的通报并非日常疫情数据统计），于是我对数据库存储的内容进行手动比较后，重新记录。此后，数据便准确了。

#### 数据补偿

我假定这个项目会一直保持运行，或在休息一段时间后重新开始运行。那么这段时间的数据如何处理？那就需要一个数据补偿机制。数据补偿机制的执行流程为：

```
爬取目录页 => 根据AccessURL表判断是否已存在数据，如果不存在则继续遍历,直到存在为止 => 爬取，入库
```

这个数据补偿方法有两种触发情况，一是**项目启动时**，二是**项目运行时的每天早上10点**。这样设计的原因是，项目启动时需要检查并更新数据，因为不能保证相较上次项目停止到底更新了多少数据；而运行时定于每天10点则是因为，卫健委的数据一般每天9点左右更新，考虑到各种可能的异常情况，10点是个比较合适的爬取时间。

### 数据处理

通过正则表达式，从文本中解析到数据是一项极其繁琐且需要细心与耐心的工作，我浏览了两年多共980篇左右的通报，总结了一些规律。然后按通报时间分类，写不同的正则表达式来匹配数据，并将数据导入到数据库中。而在数据库中存储数字比存储文字更加节省空间。所以我又将各省份名与省份编码记录在一个哈希表中，存入数据库时用省份编码代替省份名。

## 2.3 数据统计接口部分的性能改进

在项目分析与代码优化方面，我优化了生成Excel表格的方式。

最初设计的Excel生成方式，是在用户每次下载Excel表格时才读取数据库数据并写入Excel，当时采取这种设计是考虑到如果定期生成文件并下载可能会占用大量硬盘空间（每天都会有新的数据，要重新生成Excel表格）。

```java
   public void exportExcel(HttpServletRequest request, HttpServletResponse response) throws Exception {
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        String timeWord = simpleDateFormat.format(new Date());
        String fileName = "疫情数据截止_" + timeWord + ".xlsx";
        List<ExcelOutput> list = getExcelOutput();
        response.setHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode(fileName, "UTF-8"));
        EasyExcel.write(response.getOutputStream(), ExcelOutput.class).sheet("疫情数据表").doWrite(list);
        response.flushBuffer();
    }
```

其中getExcelOutput()方法的功能是获取数据库数据，并生成对应的Excel行（Excel导出功能基于Easy Excel）。

```java
 public List<ExcelOutput> getExcelOutput() {
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        List<ExcelOutput> outputs = new ArrayList<>();
        List<DailyTotalData> totalDataList = dailyTotalDataMapper.getTotalList();
        totalDataList.forEach(total -> {
        List<DailyProvincialData> provincialList = dailyProvincialDataMapper.getDataByDate(total.getDataDate());
//...以下省略
```

```java
public class ExcelOutput implements Serializable {

    @ExcelProperty(value = "时间", index = 0)
    private String date;

    @ExcelProperty(value = "症状",index = 1)
    private String symptom;

    @ExcelProperty(value = "全国", index = 2)
    private int nation;

    @ExcelProperty(value = "北京",index = 3)
    private int beijing;

    @ExcelProperty(value = "天津", index = 4)
    private int tianjin;
//以下省略
```

但是，由于每次导出的Excel表格都是拥有大量数据的，也就意味着每次都要花费大量的时间。在多次请求下载时，这样大量耗时显然不值得。

![优化前耗时](https://kyky-1305486145.cos.ap-guangzhou.myqcloud.com/beforeModify.png)

如上图所示，每次1.2min的响应时间对于用户而言显然是不可接受的。

所以，我修改代码，将列表的生成时间，即此方法的调用时机调整为项目启动时，同时建立一个静态变量excelOutputList，接下来这个列表将被存入这个对象中。同时，这个方法也会跟数据补偿一同在每天10点定时执行，以实现在项目持续运行时数据自动更新的功能。

```java
@Scheduled(cron = "0 0 10 * * ?")
public void startOp() throws InterruptedException {
    boolean getResult;
    do{
        Thread.sleep(200);
        getResult = spider.getNewWebsites();
    }
    while(!getResult);
    ExcelExportService.excelOutputList = exportService.getExcelOutput();
}
```

在这次修改之后，获取Excel的步骤就从提取数据+写入表格变成单纯的写入表格了（遍历列表的时间可以忽略不计）

![优化后耗时](https://kyky-1305486145.cos.ap-guangzhou.myqcloud.com/afterModify.png)

从 **1.2min 到 2.71s** ，效率提升极为显著。

## 2.5 数据可视化

我的数据可视化基于前端框架React，所有可视化组件均基于开源的Ant Design Chart进行二次开发。

![daping1](https://kyky-1305486145.cos.ap-guangzhou.myqcloud.com/daping1.jpg)

![daping2](https://kyky-1305486145.cos.ap-guangzhou.myqcloud.com/daping2.jpg)

基础组件包括以下部分：

*1.* 折线图

*2.* 条形图

*3.* 全国地图

二次开发所得，最终呈现在大屏上的部分有五个：

1. 内地七日内新增确诊折线图（左上图）
2. 内地七日内新增无症状折线图（右上图）
3. 全国昨日新增确诊数据地图（中）
4. 内地七日内新增确诊总数排名前十省份（左下图）
5. 自选时间段、自选省份新增确诊折线图（右下图）

这样的安排主要是为了能够直观的，综合的展现疫情的变化情况。首先，展现全国的总量变化后，再通过全国地图来展现全国各省疫情的严重程度。

其次，提供七日内的全国各省疫情数据排名，可以让访问者明确当下疫情最严重的地区，并籍此对自己的出行计划进行调整，等等。

最后，提供全国各省和时间段的选择是为了能够给用户提供查询更多更具体数据的渠道，方便大家了解不同时间段各地区的疫情数据变化。

# 三、心得体会

在这次项目里，我学了很多东西，也做了很多。这是对我的综合考验和提升良机。我巩固运用了自己的Java技术，对Spring Boot的开发方式有了更深的理解，同时也学习了更多SQL语句（Count函数，Group By语句等等），还首次尝试了使用React进行开发，感觉效果不错。最重要的是，挑战了自己，初步学习了爬虫的使用方式，这是我以前从来没有用过的技术。总的而言，这个项目确实对我来说是个很大的挑战，这两个星期确实特别辛苦，但也收获满满。唯一的遗憾是，最终没有时间研究并实现每日热点算法。如果以后有时间我会认真思考一下。

