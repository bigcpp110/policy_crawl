from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import jsbeautifier
import js2py
import requests
from copy import deepcopy
import time
from pyquery import PyQuery as pq


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
}



def gethtml(url):
    response = requests.get(url, headers=headers)
    return response


def get_cookie(url,selector,key1="FSSBBIl1UgzbN7N80S",key2="FSSBBIl1UgzbN7N80T"):
    profile = webdriver.FirefoxOptions()
    profile.add_argument('-headless')  # 设置无头模式
    driver=webdriver.Firefox(options=profile)
    driver.get(url)
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
    a=driver.get_cookie(key1)
    b=driver.get_cookie(key2)
    cookies={key1:a["value"],key2:b["value"]}
    html=driver.page_source
    driver.quit()
    return cookies

def get_html(url,selector):
    profile = webdriver.FirefoxOptions()
    profile.add_argument('-headless')  # 设置无头模式
    driver=webdriver.Firefox(options=profile)
    driver.get(url)
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
    time.sleep(1)
    html=driver.page_source
    driver.quit()
    return html


def get_url(url):
    try:
        response = gethtml(url)
        res = response.content.decode()
        js = re.compile('<script type="text/javascript">(.+?_0x33f22a\(\));', re.S).findall(res)[0]
        js = re.sub(
            "if\(_0x532424\['LaaBO'\]\(wzwsmethod,_0x532424\[_0x56ae\('0x3b','Q@8l'\)\]\)\)\{_0x2ff265\(_0x35ace3,wzwsparams\);\}else\{window\[_0x56ae\('0x3c','\)9A&'\)\]=_0x35ace3;\}",
            "return _0x35ace3", js)
        js = jsbeautifier.beautify(js)
        wzwschallenge = js2py.eval_js(js)
        cookies = response.cookies.get_dict()
        headers_new=deepcopy(headers)
        headers_new["Cookie"]="wzws_cid="+cookies["wzws_cid"]
        return wzwschallenge,headers_new
    except:
        print("再来一次")
        time.sleep(1)
        wzwschallenge,headers_new=get_url(url)
        return wzwschallenge,headers_new


def get_form_data(html,i):
    data={}
    doc=pq(html)
    data["__VIEWSTATE"]=doc("#__VIEWSTATE").attr("value")
    data["__VIEWSTATEGENERATOR"]=doc("#__VIEWSTATEGENERATOR").attr("value")
    data["__EVENTTARGET"]="AspNetPager1"
    data["__EVENTARGUMENT"]=i
    data["__EVENTVALIDATION"]=doc("#__EVENTVALIDATION").attr("value")
    data["_title"]=""
    data["_wenhao"]=""
    data["start"]=""
    data["end"]=""
    return data