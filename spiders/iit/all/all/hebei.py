import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河北省税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("#tit_name").text()
    data["content"]=doc(".TRS_Editor").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_Editor a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="河北省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a style="width:auto;" href="(.+?)" target="_blank">',html)
    for url in urls:
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,298):
        print(i)
        url="http://wzyy.hebei.chinatax.gov.cn/was5/web/search?page="+str(i)+"&channelid=245955&searchword=docchannel%3D45812&keyword=docchannel%3D45812&perpage=10&outlinepage=10"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()