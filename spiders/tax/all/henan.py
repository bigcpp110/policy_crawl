import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


#http://henan.chinatax.gov.cn/003/wd.html?DFWJ_ID=180615092227038&LM_ID=31001
def parse_index(html):
    items=eval(re.findall("({.+})",html)[0])
    for item in items["data"]:
        data = {}
        data["title"] = item["DFWJ_BT"]
        data["content"] = item["DFWJ_NR"]
        data["content_url"] = ""
        data["classification"] = "河南省税务局"
        data["publishTime"]=item["DFWJ_FBRQ"]
        data["url"] = "http://henan.chinatax.gov.cn/003/wd.html?DFWJ_ID="+ item["DFWJ_ID"] +"&LM_ID=" + item["LM_ID"]
        print(data)
        save(data)

def main():
    for i in range(1,29):
        print(i)
        url="http://henan.chinatax.gov.cn/zxhd/cms/dfwj/getNRGL_DFWJQT.do?callback=jQuery110204354242861982103_1583827086500&CURPAGE="+str(i)+"&PAGESIZE=15&LM_ID=31001&DFWJ_FBZT=1&ORDERBY=FBRQ+DESC&_=1583827086503"
        html=get(url)
        parse_index(html)

if __name__ == '__main__':
    main()