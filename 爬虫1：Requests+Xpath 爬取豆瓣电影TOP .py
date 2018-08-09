
# coding: utf-8

# In[7]:


# 1 Requests+Xpath 菜鸟爬取豆瓣TOP 
# 电影名称

'''
Requests+Xpath 爬取豆瓣电影

安装 Python 应用包
pip install requests
pip install lxml

获取元素的Xpath信息并获得文本：

手动获取：定位目标元素，在网站上依次点击：右键 > 检查
file=s.xpath('元素的Xpath信息/text()') 

快捷键“shift+ctrl+c”，移动鼠标到对应的元素时即可看到对应网页代码：

在电影标题对应的代码上依次点击 右键 > Copy > Copy XPath，获取电影名称的Xpath：


'''

import requests 
from lxml import etree


url = 'https://book.douban.com/top250'
data = requests.get(url).text
s=etree.HTML(data)


film=s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tr/td[2]/div[1]/a/@title')
print(film)



# In[1]:


# 2 全部书名

'''
浏览器经常会自己在里面增加多余的 tbody 标签，我们需要手动把这些标签删掉。


分别复制《追风筝的人》、《小王子》、《围城》、《解忧杂货店》的 xpath 信息进行对比：

//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div[1]/a
//*[@id="content"]/div/div[1]/div/table[2]/tbody/tr/td[2]/div[1]/a
//*[@id="content"]/div/div[1]/div/table[3]/tbody/tr/td[2]/div[1]/a
//*[@id="content"]/div/div[1]/div/table[4]/tbody/tr/td[2]/div[1]/a

比较可以发现书名的 xpath 信息仅仅 table 后的序号不一样，并且跟书的序号一致，于是去掉序号（去掉 tbody），我们可以得到通用的 xpath 信息：

//*[@id=“content”]/div/div[1]/div/table/tr/td[2]/div[1]/a


'''

import requests 
from lxml import etree


url = 'https://book.douban.com/top250'
data = requests.get(url).text
s=etree.HTML(data)


file=s.xpath('//*[@id="content"]/div/div[1]/div/table/tr/td[2]/div[1]/a/@title')

for title in file:
    print(title)


# In[4]:



# 3 爬取页面多个信息时的数据准确匹配问题

# strip(“(”) 表示删除括号， strip() 表示删除空白符。

'''

问题：我们默认书名和评分是正确的信息,如果某一项少爬或多爬了信息，匹配错误


思路：书名的标签肯定在这本书的框架内，以每本书为单位，分别取获取对应的信息，完全匹配

//*[@id=“content”]/div/div[1]/div/table[1]   #整本书
//*[@id=“content”]/div/div[1]/div/table[1]/tr/td[2]/div[1]/a   #书名
//*[@id=“content”]/div/div[1]/div/table[1]/tr/td[2]/div[2]/span[2]   #评分

我们发现，书名和评分 xpath 的前半部分和整本书的 xpath 一致的， 那我们可以通过这样写 xpath 的方式来定位信息：

file=s.xpath(“//*[@id=“content”]/div/div[1]/div/table[1]”)
title =div.xpath(“./tr/td[2]/div[1]/a/@title”)
score=div.xpath(“./tr/td[2]/div[2]/span[2]/text()”)

'''


import requests 
import time
from lxml import etree


url = 'https://book.douban.com/top250'
data = requests.get(url).text
s=etree.HTML(data)

file=s.xpath('//*[@id="content"]/div/div[1]/div/table')

for div in file:
    title = div.xpath("./tr/td[2]/div[1]/a/@title")[0]
    href = div.xpath("./tr/td[2]/div[1]/a/@href")[0]
    score = div.xpath("./tr/td[2]/div[2]/span[2]/text()")[0]
    num = div.xpath("./tr/td[2]/div[2]/span[3]/text()")[0].strip("(").strip().strip(")")
    scribe = div.xpath("./tr/td[2]/p[2]/span/text()")
    
    time.sleep(2)
    
    print("{}{}{}{}{}".format(title,href,score,num,scribe[0]))



# In[6]:


# 翻页
'''
https://book.douban.com/top250?start=0 #第一页
https://book.douban.com/top250?start=25 #第二页
https://book.douban.com/top250?start=50 #第三页

以每页25为单位，递增25，只是 start=()的数字不一样

写一个循环

for a in range(3):    
  url = 'https://book.douban.com/top250?start={}'.format(a*25)
  #3个页面，用 a*25 保证以25为单位递增
  
'''

import requests 
import time 
from lxml import etree


for a in range(3):
    url = 'https://book.douban.com/top250?start={}'.format(a*25)
    data = requests.get(url).text

    s=etree.HTML(data)
    file=s.xpath('//*[@id="content"]/div/div[1]/div/table')
    time.sleep(3)

    for div in file:
        title = div.xpath("./tr/td[2]/div[1]/a/@title")[0]
        href = div.xpath("./tr/td[2]/div[1]/a/@href")[0]
        score=div.xpath("./tr/td[2]/div[2]/span[2]/text()")[0]
        num=div.xpath("./tr/td[2]/div[2]/span[3]/text()")[0].strip("(").strip().strip(")").strip()
        scrible=div.xpath("./tr/td[2]/p[2]/span/text()")

        if len(scrible) > 0:
            print("{},{},{},{},{}\n".format(title,href,score,num,scrible[0]))
        else:
            print("{},{},{},{}\n".format(title,href,score,num))






