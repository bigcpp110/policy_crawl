import re
import time
import json

from selenium import webdriver
from bs4 import BeautifulSoup

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
import pandas as pd


def parse_detail(html,url):
    alllog.logger.info("北京民政局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="北京民政局"
    data["url"]=url
    print(data)
    # save(data)

def parse_index(html):
    urls=re.findall("urls\[i\] = '(.+?)';",html)
    for url in urls:
        if "http" not in url:
            url="http://mzj.beijing.gov.cn/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main2():
    for i in range(0,1):
        print(i)
        url="http://mzj.beijing.gov.cn/col/col6112/index.html"
        html=get(url)
        parse_index(html)
    for i in range(0, 1):
        print(i)
        url = "http://mzj.beijing.gov.cn/col/col4492/index.html"
        html = get(url)
        parse_index(html)

url = 'http://sousuo.gov.cn/data?t=zhengcelibrary&q=%E7%96%AB%E6%83%85&timetype=' \
      '&mintime=&maxtime=&sort=&sortType=1&searchfield=title&pcodeJiguan=&childtype=' \
      '&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={}&n=5&inpro=&bmfl=&dup=&orpro='

types = ['gongwen', 'bumenfile', 'otherfile', 'gongbao']

def remove_style(x):
    x = x.replace('<em>','')
    x = x.replace('</em>','')
    x = x.replace('<br>','')
    return x


# 打开chrome浏览器
# 加载启动项
option = webdriver.ChromeOptions()
option.add_argument('headless')
#driver = webdriver.Chrome(chrome_options=option)

rs_list = []
def main():
    for i in range(0,41):
        page_url = url.format(i)
        print(page_url)

        # driver.get(url=page_url)
        # time.sleep(2)
        # html = driver.page_source
        # soup = BeautifulSoup(html, 'lxml')
        # #cc = soup.select('pre')[0]
        # rs = json.loads(soup.select('pre')[0])

        rs = json.loads(get(page_url))
        time.sleep(3)
        #print(rs['searchVO']['catMap'].keys())
        for t in types:
            tls = rs['searchVO']['catMap'][t]['listVO']
            for item in tls:
                #print('{}|{}|{}|{}|{}'.format(item['title'],item['pubtimeStr'],item['url'],item['puborg'],item['subjectword']))
                rs_list.append((item['pubtimeStr'],t,item['title'],item['url'],item['puborg'],item['childtype'],item['subjectword']))
    rs_df = pd.DataFrame(rs_list)
    rs_df.columns = ['pubtime','type','title','url','puborg','childtype','subjectword']
    rs_df['pubtime'] = rs_df.pubtime.apply(lambda x: x.replace('.','-'))
    rs_df['title'] = rs_df.title.apply(lambda x:remove_style(x))
    rs_df['pubtime'] = pd.to_datetime(rs_df['pubtime'])
    rs_df = rs_df.sort_values('pubtime',ascending=False)
    print(rs_df.pubtime.head())
    print(rs_df.shape)
    rs_df.columns = ['发布时间','类型','标题',  'url', '发文机关', '主题分类', '主题词']
    rs_df.to_excel('摘要.xlsx',index=False)
    #rs_df.to_csv('摘要.csv',index=False)

content_ls =[]
def get_content():
    rs_df = pd.read_excel('摘要.xlsx')
    print(rs_df.head())
    for u in rs_df['url']:
        doc = pq(get(u))
        time.sleep(3)
        content = doc(".pages_content").text()
        if len(content) == 0:
            content = doc("#UCAP-CONTENT").text()
        print('{},{}'.format(len(content), u))
        content_ls.append(content)

    rs_df['正文'] = content_ls
    rs_df.to_excel('政策内容.xlsx', index=False)



if __name__ == '__main__':
    #main()
    get_content()
    # driver = webdriver.Chrome()
    # base_url = 'https://www.baidu.com'
    # driver.get(base_url)