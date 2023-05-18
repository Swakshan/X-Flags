import requests
import json
from bs4 import BeautifulSoup as bs
from user_agent import generate_user_agent
from pprint import pprint
from urllib.parse import unquote
from datetime import datetime
from comman import WEB_LINK,M_WEB_LINK


hdr = {'User-Agent': generate_user_agent(os="android")}


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


class Aptiode():
    def __init__(self, pkgName, limit=30):
        self.siteUrl = f"https://ws75.aptoide.com/api/7/app/get/package_name={pkgName}/limit={limit}/aab=true"

    def versions(self):
        rd = {'appName': "", 'data': {}, "status": False}
        try:
            url = self.siteUrl
            req = requests.get(url, headers=hdr)
            if req.status_code != 200:
                rd['reason'] = req.status_code
                return rd
            pkjson = req.json()
            nodes = pkjson['nodes']
            baseAppName = nodes['meta']['data']['name']

            wData = {}
            lists = nodes['versions']['list']
            for item in lists:
                data = {}
                apk_id = item['id']
                pkgName = item['package'].replace('.', '-')
                store_name = item['store']['name']
                file = item['file']
                vername = file['vername']
                vercode = file['vercode']
                md5sum = file['md5sum']
                typ = "alpha" if "alpha" in vername else "beta" if "beta" in vername else "stable"
                apk_type = "apk"
                updtime = file['added']
                link = f"https://pool.apk.aptoide.com/{store_name}/{pkgName}-{vercode}-{apk_id}-{md5sum}.apk"

                data['vername'] = vername
                data['vercode'] = vercode
                data['type'] = typ
                data['apk-type'] = apk_type
                data['upd'] = updtime
                data['link'] = unquote(link)

                if typ not in wData:
                    # data = DATA(name=baseAppName,vername=vername,vercode=vercode,app_id=apk_id,typ=typ,link=link,upd=0)
                    wData[typ] = data

                if len(wData) == 3:
                    wData[typ] = data
                    break
                # whole.append(data)

            rd['status'] = True
            rd['data'] = wData
            rd['appName'] = baseAppName

        except Exception as e:
            # e = get_exception()
            rd['status'] = False
            rd['reason'] = str(e)
        return rd


class TwtWeb():
    def __init__(self) -> None:
        url = M_WEB_LINK
        req = requests.get(url, headers=hdr)
        if req.status_code != 200:
            url = "https://api.allorigins.win/raw?url="+M_WEB_LINK
            req = requests.get(url, headers=hdr)
            if req.status_code != 200:
                self.webData = False
            else:
                self.webData = req.text
        else:
            self.webData = req.text

    def jsonFinder(self, startData):
        endData = '};'
        pS = self.webData
        if not pS:
            return False
        s = pS.find(startData)+len(startData)+1
        e = pS[s:].find(endData)+1+s
        data = pS[s:e]
        return json.loads(data)

    def version(self):
        startData = 'window.__META_DATA__'
        rd = self.jsonFinder(startData)
        if not rd:
            return rd, False

        sha = rd['sha']
        version = rd['cookies']['version']
        return version, sha

    def featureSwitches(self):
        startData = 'window.__INITIAL_STATE__'
        fs = self.jsonFinder(startData)['featureSwitch']
        configs = fs['defaultConfig']
        fs_token = fs['featureSetToken']
        if not fs:
            return False
        return {"default": {'feature_set_token':fs_token,'config': configs}}
