import time
import random
import requests
from my_fake_useragent import UserAgent

from policy_crawl.common.logger import errorlog
headers={"User-Agent":UserAgent().random()}

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
