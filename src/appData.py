import requests
import json
from bs4 import BeautifulSoup as bs
from pprint import pprint
from urllib.parse import unquote
from datetime import datetime
from common import WEB_LINK,M_WEB_LINK,TWT_SW_URL,headers


hdr = headers()
proxyUrl = "https://translate.google.com/website?sl=ta&tl=en&hl=en&client=webapp&u="

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


def apkM(url):
    url = proxyUrl+url
    res = requests.get(url,headers=hdr)

    pS = bs(res.text,"html.parser")
    downloadBtn = pS.find("a",{"class":"downloadButton"})
    downloadPage = downloadBtn['href']
    downloadBtnText = downloadBtn.text.strip().lower()
    is_bundle = True if "apk bundle" in downloadBtnText else False

    res = requests.get(downloadPage,headers=hdr)
    pS = bs(res.text,"html.parser")

    downloadLink = pS.find("a",{'id':'download-link'})['href']
    downloadLink = downloadLink.replace("www-apkmirror-com.translate.goog","www.apkmirror.com").replace("&_x_tr_sl=ta&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp","")
    return is_bundle,downloadLink


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