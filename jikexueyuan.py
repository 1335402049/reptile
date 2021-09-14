import importlib,sys
import re
import requests

importlib.reload(sys)

class jikexueyuan(object):
    def __init__(self):
        print ('开始爬虫......')

    # 抓取网页html
    def getSource(self,url):
        html = requests.get(url)
        return html.text

    #生成需要抓取的网页列表
    def changePage(self,url,total_page):
        page_group = []
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def getEveryClass(self,html):
        every_class = re.findall('(<li id=.*?</li>)',html,re.S)
        return every_class

    def getInfo(self,everyclass):
        info = {}
        info['title'] = re.search('class="lessonimg" title="(.*?)"',everyclass,re.S).group(1)
        info['link'] = re.search('<a href="(.*?)"',everyclass,re.S).group(1).strip('//')
        info['summary'] = re.search('display: none;">(.*?)</p>',everyclass,re.S).group(1).strip()
        return info

    def writeContent(self,info):
        with open('E:\\test.txt', 'a', encoding='utf-8') as f:
            f.write(info['title'] + '\n')
            f.write(info['link'] + '\n')
            f.write(info['summary'] + '\n')
            f.write('\n')

if __name__ == '__main__':
    url = 'https://www.jikexueyuan.com/course/?pageNum=1'
    #实例化class
    jike = jikexueyuan()
    #生成前20页网页列表
    all_links = jike.changePage(url,20)
    for link in all_links:
        html = jike.getSource(link)
        every_class = jike.getEveryClass(html)
        for each in every_class:
            info = jike.getInfo(each)
            jike.writeContent(info)
