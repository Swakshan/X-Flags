import requests
import json
from bs4 import BeautifulSoup as bs
from user_agent import generate_user_agent
from pprint import pprint
from urllib.parse import unquote
from datetime import datetime
from common import WEB_LINK,M_WEB_LINK,TWT_SW_URL


hdr = {'User-Agent': generate_user_agent()}


class ApkCombo():
    def __init__(self, pkgName, company='', proxy=1) -> None:
        self.hdr = hdr
        proxyUrl = ""
        if proxy:
            proxyUrl = "https://translate.google.com/website?sl=ta&tl=en&hl=en&client=webapp&u="
        self.siteUrl = "https://apkcombo.com"
        self.company = company
        self.package_name = pkgName

        self.apkUrl = f'{proxyUrl}{self.siteUrl}/{company}/{pkgName}'
        self.apkUrl = f'{proxyUrl}{self.siteUrl}/search/{pkgName}'
        self.apkVerUrl = self.apkUrl+"/old-versions?page={page}"
        self.apkDownUrl = self.apkUrl+'/download/phone-{vername}-apk'

        self.proxyUrl = proxyUrl

    def versions(self, page=1):
        rd = {}
        try:
            site = self.siteUrl
            url = self.apkVerUrl.format(page=page)
            hdr = self.hdr

            req = requests.get(url, headers=hdr)
            if req.status_code != 200:
                rd['status'] = False
                rd['reason'] = req.status_code
                return rd

            # txt = req.json()['contents']
            txt = req.text
            pS = bs(txt, 'html.parser')

            baseAppName = pS.title.text.replace(' - Old Versions APK', "")

            ver_list = pS.find('ul', attrs={'class': 'list-versions'})
            items = ver_list.find_all('li')

            wData = {}
            whole = []
            for item in items:
                data = {}
                a = item.find('a')

                nameSec = a.find('span', attrs={'class': 'vername'})
                name = nameSec.text
                typSec = nameSec.find('span', attrs={'class': 'blur'})

                typ = "stable" if typSec is None else typSec.text
                name = name if typSec is None else name.replace(" "+typ, "")
                apk_type = a.find('span', attrs={'class': 'type-apk'})
                if not apk_type:
                    apk_type = a.find('span', attrs={'class': 'type-xapk'})
                apk_type = apk_type.text
                updtime = a.find(
                    'div', attrs={'class': 'description'}).text.split(' ·')[0]
                # link  = site+a['href']
                vername = name.replace(baseAppName, "").strip()
                link = self.apkDownUrl.format(vername=vername)

                # data['name'] = name
                data['vername'] = vername
                data['type'] = typ
                data['apk-type'] = apk_type
                data['upd'] = updtime
                data['link'] = link

                if typ not in wData:
                    wData[typ] = data

                if len(wData) == 3:
                    wData[typ] = data
                    break
                # whole.append(data)

            rd['status'] = True
            rd['data'] = wData
            rd['appName'] = baseAppName
        except Exception as e:
            rd['status'] = False
            rd['reason'] = str(e)
        return rd

    def getApk(self, vername, variant="apk"):
        rd = {}
        try:
            url = self.apkDownUrl.format(vername=vername)
            hdr = self.hdr
            # print(url)
            req = requests.get(url, headers=hdr)
            if req.status_code != 200:
                rd['status'] = False
                rd['reason'] = req.status_code
                return rd
            txt = req.text
            pS = bs(txt, 'html.parser')

            file_list = pS.find_all('ul', attrs={'class': 'file-list'})

            file_list = file_list[0]
            details = file_list.find('li')
            link = details.find('a')['href']+'&fp=howareyou123&ip=0.0.0.0.0'
            link = link.replace(
                self.proxyUrl, '') if self.proxyUrl in link else link

            vercode = pS.find('span', attrs={'class': 'vercode'})
            vercode = vercode.text[1:len(
                vercode.text)-1] if not vercode is None else '0'
            
            apkType = pS.find('span', attrs={'class': 'vtype'}).text.strip().lower()
            
            wData = {
                'link': unquote(link),
                'vercode': vercode,
                'apktype': apkType
            }
            rd['status'] = True
            rd['data'] = wData
        except Exception as e:

            rd['status'] = False
            rd['reason'] = str(e)
        return rd


class TwtWeb():
    def __init__(self) -> None:
        req = requests.get(TWT_SW_URL,headers=hdr)
        res = req.text

        sHint = 'self.__META_DATA__ = '
        eHint = "}"
        s = res.find(sHint)+len(sHint)
        e = res[s:].find(eHint)+s+1
        self.config = json.loads(res[s:e])

                
        txt = res[res.find("["):res.find("]")+1]
        js_list = json.loads(txt)

        for item in js_list:
          if "feature-" in item:
            self.FS_URL = item
            break
    
    def version(self):
        rd = self.config

        sha = rd['sha']
        version = int(datetime.now().timestamp())
        return sha, version

    def featureSwitches(self):
      fs = ""
      req = requests.get(self.FS_URL,headers=hdr)
      res = req.text   
      res = res.replace("!0","true").replace("!1","false")
    #   fs = js2py.eval_js(res).to_dict()
      return fs


def webfeatureSwitches(hash):
      FS_URL = f"https://abs.twimg.com/responsive-web/client-web/feature-switch-manifest.{hash}.js"
      req = requests.get(FS_URL,headers=hdr)
      res = req.text
      res = res[res.find("{"):res.find("}}};")]

      res = res.replace("!0","true").replace("!1","false")
      res = res.replace("},",'},"').replace(':{value:','":{"value":').replace(':{name:','":{"name":').replace(',type:',',"type":').replace(',defaultValue:',',"defaultValue":')
      res = res.replace("feature_set_token:",'"feature_set_token":').replace(',config:',',"config":').replace(',"debug:',',"debug":').replace(',enumeration_values',',"enumeration_values"')
      res = res.replace('"":','":')
      res = res+"}}}"

      fs = json.loads(res)
      return fs