import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("安徽省国有资产委员会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".s_article_top h1").text()
    if not data["title"]:
        data["title"] = doc(".dicontent_bt h1").text()
    data["content"]=doc(".h-content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".h-content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"] = doc(".dicontent_left").text().replace("\n", "")
        data["content_url"] = [item.attr("href") for item in doc(".dicontent_left a").items()]
    data["classification"]="安徽省国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc("#ul_list tr a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://gzw.ah.gov.cn/xxgk/" + url
        try:
            html=get(url,code="gbk")
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://gzw.ah.gov.cn/xxgk/list.jsp"
    for i in range(1,40):
        print(i)
        data={'strColId': '0ae0ae0d59cb48b38d86babb0edc8918', 'strTopicType': '', 'strThemeType': '', 'strWebSiteId': '1448866116912004', 'strPage': '', 'strMasTitle': '', 'year': '', '_index': '', 'PageSizeIndex': str(i), 'strIndex': '', 'strSearchContent': '', 'strTxtCnt': ''}
        html=post(url,data=data,code="gbk")
        parse_index(html)



if __name__ == '__main__':
    main()