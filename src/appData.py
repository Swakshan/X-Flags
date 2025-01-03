import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint
from urllib.parse import unquote
from datetime import datetime
from common import headers

hdr = headers()
proxyUrl = "https://translate.google.com/website?sl=ta&tl=en&hl=en&client=webapp&u="

def beautifulSoup(url,proxy=1):
    if proxy:
        url = proxyUrl+url
    print(url)
    req = requests.get(url, headers=hdr)
    if req.status_code != 200:
        raise Exception("page not found:\nURL: "+url)
    
    txt = req.text
    return bs(txt, 'html.parser')

def apkCombo(url):
    pS:bs = beautifulSoup(url)

    file_list = pS.find('ul', attrs={'class': 'file-list'})
    details = file_list.find('li')
    link = details.find('a')['href']
    if "r2?u=" in link:
        s = link.find("r2?u=")+len("r2?u=")
        link = link[s:].replace("&_x_tr_sl=ta&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp","")
    else:
        link+='&fp=howareyou123&ip=0.0.0.0.0'
        link = link.replace(proxyUrl, '')
    return unquote(link)


def apkM(url):
    pS:bs = beautifulSoup(url)
    downloadBtn = pS.find("a",{"class":"downloadButton"})
    downloadPage = downloadBtn['href']
    # downloadBtnText = downloadBtn.text.strip().lower()
    # is_bundle = True if "apk bundle" in downloadBtnText else False
    pS:bs = beautifulSoup(downloadPage,0)

    downloadLink = pS.find("a",{'id':'download-link'})['href']
    downloadLink = downloadLink.replace("www-apkmirror-com.translate.goog","www.apkmirror.com").replace("&_x_tr_sl=ta&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp","")
    return downloadLink


def webfeatureSwitches(hash):
      FS_URL = f"https://abs.twimg.com/responsive-web/client-web/feature-switch-manifest.{hash}.js"
      req = requests.get(FS_URL,headers=hdr)
      res = req.text
      res = res[res.find("{"):res.find("}}};")]

      res = res.replace("!0","true\n").replace("!1","false\n")
      res = res.replace("},",'},"').replace(':{value:','":{"value":').replace(':{name:','":{"name":').replace(',type:',',"type":').replace(',defaultValue:',',"defaultValue":')
      res = res.replace("feature_set_token:",'"feature_set_token":').replace(',config:',',"config":').replace(',"debug:',',"debug":').replace(',enumeration_values',',"enumeration_values"')
      res = res.replace('"":','":').replace(":.",":0.")
      res = res+"}}}"

      fs = json.loads(res)
      return fs