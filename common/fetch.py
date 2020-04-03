import time
import random
import requests
#from my_fake_useragent import UserAgent

from policy_crawl.common.logger import errorlog

user_agent_list = [
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
  'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]
#随机选择一个
user_agent = random.choice(user_agent_list)
#传递给header
headers = { 'User-Agent': user_agent }

#headers = {''}

def get(url,params=None,headers=headers,code="utf-8",timeout=160,**kwargs):
    res=requests.get(url,params=params,headers=headers,timeout=timeout,**kwargs)
    if res.status_code in [200,201,301]:
            return res.content.decode(code)
    else:
        errorlog.logger.error("url status_code 错误：%s,status_code:%s" % (url, res.status_code))
        raise ConnectionError("没有连接")


def post(url,data=None,headers=headers,code="utf-8",timeout=160,**kwargs):
    res=requests.post(url,data=data,headers=headers,timeout=timeout,**kwargs)
    if res.status_code in [200,201,301]:
            return res.content.decode(code)
    else:
        errorlog.logger.error("url status_code 错误：%s,status_code:%s" %(url,res.status_code))
        raise ConnectionError("没有连接")
