# An Covid-19 data analysis program based on the Health Commission(NHC) announcement
<br>

请直接下载**package.zip**解压并运行**get_result.py**以获得最好体验。

<br>

---

<br>

### **get_result.py**

> 运行后输入日期（严格按照格式：xxxx-xx-xx）后即可生成当日的新增确诊/无症状人数excel表格、柱状图、地图。
<br>

---

<br>

### **get_url.py**

> * 运行后自动爬取卫健委网站所有通报网址，以{日期:网址}的格式存入json文件中。
> * package压缩包中有已经生成好的**url_list.js**文件。
<br>

---

<br>

### **get_text.py**

> * 通过对**url_list.js**中的键进行遍历，获取网址。
> * 爬取网页内所有文字，以日期为文件名存为txt文件。
> * package压缩包中的**text_result文件夹**中有已经生成好的所有文本文件。
