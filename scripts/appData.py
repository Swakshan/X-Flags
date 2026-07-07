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

def apkPure(package_name):
    api = f"https://tapi.pureapk.com/v3/get_app_his_version?package_name={package_name}&hl=en"
    hdr['Ual-Access-Businessid'] = "projecta"
    hdr['Ual-Access-ProjectA'] = '{"device_info":{"abis":["arm64-v8a"],"os_ver":"36"}'
    req = requests.get(api, headers=hdr,timeout=5)
    if req.status_code != 200:
        raise Exception(f"ApkPure statusCode:{req.status_code}")
    res = req.json()
    item = res['version_list'][0]
    return item['asset']['url']

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

    req = requests.get(link, headers=hdr)
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


def xChatOverloadedWebFlags():
    try:
        baseLink = "https://chat.x.com"
        req = requests.get(baseLink, headers=hdr)
        res = req.text
        
        startKey = "window.__INITIAL_DATA__ = "
        endKey = "}};</"
        
        start = res.find(startKey)+len(startKey)
        end = res.find(endKey,start)+2
        
        overloadedFlags = json.loads(res[start:end])
        
        if "features" in overloadedFlags:
            return overloadedFlags['features']
    except Exception as e:
        print("FAILED: failed to fetch overloaded xchat flags")
        print(e)
    return {}

def xChatWebFeatureSwitches(hash):
    jsUrl = f"https://abs.twimg.com/x-web/xchat/assets/entry-client-{hash}.js"
    
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
    overloadedFlags = xChatOverloadedWebFlags()
    
    for ovrFlag in overloadedFlags:
        flags[ovrFlag] = overloadedFlags[ovrFlag]
        
    return {"feature_set_token":token,"config":flags,"debug":{}}


    