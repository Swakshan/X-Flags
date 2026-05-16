import requests,json,re
from bs4 import BeautifulSoup as bs
from pprint import pprint
from urllib.parse import unquote
from datetime import datetime
from constants import headers
import curl_cffi
import chompjs

hdr = headers()
proxyUrl = "https://translate.google.com/website?sl=ta&tl=en&hl=en&client=webapp&u="

def beautifulSoup(url,proxy=1):
    if proxy:
        url = proxyUrl+url
    
    req = curl_cffi.get(url, impersonate="chrome")
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

#Credits: HerrErde/SubwaySurfers-Api
def apkPure(package_name,version):
    api = f"https://api.pureapk.com/m/v3/cms/app_version?hl=en-US&package_name={package_name}"
    hdr['x-sv'] = "29"
    hdr['x-abis'] = "arm64-v8a"
    hdr['x-gp'] = "1"
    
    req = requests.get(api, headers=hdr)
    if req.status_code != 200:
        raise Exception("apkPure API failed")
    res = re.findall(rb"[\x20-\x7E]{4,}", req.content)
    apkPversion:str = res[3].decode("utf-8")
    if not apkPversion.startswith(version):
        print(apkPversion,version,end="\n")
        raise Exception("apkPure API doesnt have "+version)
    return res[11].decode("utf-8")

def apkM(url):
    pS:bs = beautifulSoup(url,0)
    downloadBtn = pS.find("a",{"class":"downloadButton"})
    if not downloadBtn.find("span"):
        redirectUrl = pS.find("div",{"class":"dowrap-break-all"}).find("a")['href']
        urlSp = redirectUrl.split("/")
        downUrl = url+"/"+urlSp[len(urlSp)-2]
        return apkM(downUrl)
    downloadPage = downloadBtn['href']
    pS:bs = beautifulSoup(downloadPage,0)

    downloadLink = pS.find("a",{'id':'download-link'})['href']
    downloadLink = downloadLink.replace("www-apkmirror-com.translate.goog","www.apkmirror.com").replace("&_x_tr_sl=ta&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp","")
    return downloadLink


def formatWebFlags(res):
    res = res.replace("!0","true\n").replace("!1","false\n")
    return chompjs.parse_js_object(res)
    
def xManifestSwitches(hash):
    FS_URL = f"https://abs.twimg.com/responsive-web/client-web/feature-switch-manifest.{hash}.js"
    req = requests.get(FS_URL,headers=hdr)
    res = req.text
    eHint = "}}};"
    res = res[res.find("{"):res.find(eHint)+len(eHint)]
    return formatWebFlags(res)

def xWebFlags():
    link = "https://x.com"
    url = f"{proxyUrl}{link}"
    
    req = requests.get(url, headers=hdr)
    res = req.text

    sHint = "window.__INITIAL_STATE__="
    eHint = "window.__META_DATA__="
    s = res.find(sHint) + len(sHint)
    e = res[s:].find(eHint) + s - 1
    fd = res[s:e]
    flagData = json.loads(fd)
    featureSwitch = flagData['featureSwitch']
    token = featureSwitch["featureSetToken"]
    
    defaultConfig = featureSwitch['defaultConfig']
    userFlag = featureSwitch['user']['config']
    
    flags = {**defaultConfig, **userFlag}
    return {"feature_set_token":token,"config":flags}

def webfeatureSwitches(hash):    
    xFlags = xWebFlags()
    manifestFlags = xManifestSwitches(hash)
    flags = {**xFlags['config'],**manifestFlags['config']}
    token = xFlags['feature_set_token']

    return {"feature_set_token":token,"config":flags,"debug":manifestFlags['debug']}


def xChatWebFeatureSwitches(hash):
    jsUrl = f"https://chat.x.com/assets/entry-client-{hash}.js"
    
    req = requests.get(jsUrl, headers=hdr)
    res = req.text
    
    sHint = "window.__INITIAL_DATA__?.dtabLocal"
    res = res[res.find(sHint):]
    
    sHint = "=`"
    eHint = "`,"
    start = res.find(sHint)+len(sHint)
    token = res[start:res.find(eHint)]
    
    eHint = "}),"
    res = res[start:]
    res = res[res.find("{"):res.find(eHint)+len(eHint)]
    
    flags = formatWebFlags(res)
    return {"feature_set_token":token,"config":flags,"debug":{}}
    
    