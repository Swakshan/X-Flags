import os,json
from user_agent import generate_user_agent
from enum import Enum
from sys import exc_info
from traceback import format_exception
from dotenv import load_dotenv
from model import Source,Platform,Releases

load_dotenv()

def getEnv(key):
    return os.environ.get(key)
  

APP_NAME = "Twitter"
PKG_NAME = 'com.twitter.android'
DUMMY_FOLDER = './dummy/'
ZIP_FILE = DUMMY_FOLDER+'app.zip'

EXTRACT_FOLDER = DUMMY_FOLDER+'Extracted/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

old_file_name = MAIN_FOLDER+'old_feature_data.json'
new_file_name = MAIN_FOLDER+'new_feature_data.json'
old_file_ipad_name = MAIN_FOLDER+'old_feature_ipad_data.json'
new_file_ipad_name = MAIN_FOLDER+'new_feature_ipad_data.json'
manifest_file_name = "manifest.json"
NEW_FLAG_LIMIT = 25

USERNAME = "Swakshan"
REPO_NAME = "X-Flags"
DEBUG  =  int(getEnv("DEBUG"))
SHA = getEnv('GIT_COMMIT_SHA')
CHANNEL_ID =  getEnv('CHANNEL_ID')
PIN_MSG =  getEnv('PIN_MSG')
BOT_TOKEN = getEnv('BOT_TOKEN')


WEB_LINK = 'https://twitter.com/'
M_WEB_LINK = 'https://m.twitter.com/'
TWT_SW_URL = f"{WEB_LINK}sw.js"
APP_STORE_LINK = "https://apps.apple.com/in/app/x/id333903271"

def get_exception():
    etype, value, tb = exc_info()
    info, error = format_exception(etype, value, tb)[-2:]
    return f'Exception in: {info}: {error}'

def printJson(data):
    print(json.dumps(data,indent=4))

def readFile(filename):
    f = open(filename,'r',encoding='utf-8')
    d = f.read()
    f.close()
    return d

def writeFile(fileName,data):
    f = open(fileName, 'w')
    f.write(data)
    f.close()

def writeJson(fileName,data):
    f = open(fileName, 'w')
    json.dump(data,f,indent=4)
    f.close()

def readJson(filename):
    f = open(filename,'r')
    d = json.load(f)
    f.close()
    return d

def printLine():
    return "*--------------*"

def vercodeGenerator(v):
    vCode = "20" if "alpha" in v else "10" if "beta" in v else "00"
    vercode = v.replace("-alpha.",vCode).replace("-beta.",vCode).replace("-release.",vCode)
    vercode = "3"+vercode.replace(".","")
    return vercode

def headers():
    return {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": generate_user_agent(),
}

def commitLinkFormat(flag_data):
    def countFormat(count,ns="Flags"):
        if not count:
            return False
        
        f = ns if count>1 else ns[:-1]
        return f"{count} {f}"
    
    msg = ""
    for key in flag_data:
        flag_det = flag_data[key]
        ns = key.title().replace("_"," ")
        for func in flag_det:
            flags = flag_det[func]
            lf = len(flags)
            if func == "added" and lf<NEW_FLAG_LIMIT:
                continue
            fStr = countFormat(lf,ns)
            if fStr:
                msg = f"{msg} and {fStr} {func.title()}"
    
    msg = msg[5:] if len(msg) else "Repo Link"
    return msg

def strpattern(flag_details,flag_details_2):
    manifest_file = readJson(manifest_file_name)
    vername = manifest_file['version_name']
    vercode = manifest_file['vercode']
    down_link = manifest_file['download_link']
    hash_value = manifest_file['hash']
    platform = Platform(manifest_file['os'])
    source = Source(manifest_file['src'])
    release = Releases.STABLE if "web" in vername else Releases.BETA if "beta" in vername else Releases.ALPHA if "alpha" in vername else Releases.STABLE
    
    global linkRow,linkCount
    linkRow = "";linkCount=0
    def linkRowFormer(name,link):
        global linkRow,linkCount
        tempLink = f'[{name}]({link})'
        linkRow+=tempLink
        if linkCount%2==0:
            linkRow+=" | "
        else:
            linkRow+="\n"
        linkCount+=1

    def setHashtag(txt:Enum):
        return "#"+txt.value

    nf = "";df=""
    flag_data = flag_details['flags']
    new_flags = dict(list(flag_data['added'].items())[:NEW_FLAG_LIMIT])
    for f in new_flags:
        value = new_flags[f]
        ty = type(value).__name__
        nf = f'• `{f}` :{ty}\n{nf}'
    nfC = len(new_flags)

    debug_flag_data =flag_details['debug_flags']
    debug_flags = debug_flag_data['added'][:NEW_FLAG_LIMIT]
    for f in debug_flags:
        df = f'• `{f}`\n{df}'
    dfC = len(debug_flags)

    commit_link_str = commitLinkFormat(flag_details)
    commit_link_str_2 = False
    pin_link = f"https://t.me/c/{CHANNEL_ID}/{PIN_MSG}"
    # platformRow = f"_Platform_: `{platform.title()}`"
    hastags = setHashtag(platform)+" "+setHashtag(release)
    vercode_str = ""
    if platform == Platform.ANDROID:
        vercode_str = f"__Vercode__:\n`{vercode}`" if int(vercode) else vercode_str #if not "0"
        ps_link = 'https://play.google.com/store/apps/details?id='+PKG_NAME
        apkc_link = f'https://apkcombo.app/search/{PKG_NAME}/download/phone-{vername}-apk'
        apkf_link = f'https://apkflash.com/apk/app/{PKG_NAME}/twitter/download/{vername}'
        apkp_link = f'https://d.apkpure.com/b/XAPK/{PKG_NAME}?versionCode={vercode}'
        apkm_vername = vername.replace('.','-')
        apkm_link = f'https://www.apkmirror.com/apk/x-corp/x/twitter-{apkm_vername}-release/x-previously-twitter-{apkm_vername}-android-apk-download'

        linkRowFormer("Play Store",ps_link)
        linkRowFormer("APKMirror",apkm_link)
        linkRowFormer("APKCombo",apkc_link)
        linkRowFormer("APKFlash",apkf_link)
        # linkRow = f'[Play Store]({ps_link}) | [APKMirror]({apkm_link})\n[APKCombo]({apkc_link}) | [APKFlash]({apkf_link})\n'
        if "release" in vername:
            linkRowFormer("APKPure",apkp_link)
        if source == Source.APT:
            linkRowFormer("Aptoide",down_link)
            linkRow = f'{linkRow}\n*\\[⚠️APK from Aptoide is known for crashes⚠️\\]*\n'
        
        linkRow = linkRow+"\n" if linkRow[-2]=="|" else linkRow

    elif platform == Platform.IOS:
        # platformRow = f"_Platform_: `{platform.upper()}`"
        linkRow = f"[App Store]({APP_STORE_LINK})\n"
        if flag_details_2:
            commit_link_str_2 = commitLinkFormat(flag_details_2)
     
    elif platform == Platform.WEB:
        vername = vername.title()
        vercode_str = f"__Hash__:\n`{hash_value}`"
        linkRow = f"[Web Link]({WEB_LINK})\n"
        hastags = setHashtag(platform)


    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=split"
    l = printLine()
    # rd = f"⚠️`{vername}`⚠️\n\n{platformRow}\n"
    rd = f"⚠️`{vername}`⚠️\n"
    rd = rd if not len(vercode_str) else f"{rd}{vercode_str}\n"
    rd = f'{rd}\n{linkRow}\n[Other Version Details]({pin_link})\n{l}'
    if nfC:
        rd = f'{rd}\n__New Flags__'
        rd = f'{rd}\n{nf}\n{l}'
    if dfC:
        rd = f'{rd}\n__New Debug Flags__'
        rd = f'{rd}\n{df}\n{l}'
    elif not nfC and not dfC:
         rd = f"{rd}\nNo New Flags\n{l}"
    if commit_link_str_2:
        rd = f'{rd}\n_iPhone:_\n[{commit_link_str}]({commit_link})\n'
        rd = f'{rd}\n_iPad:_\n[{commit_link_str_2}]({commit_link})\n{l}'
    else:
        rd = f'{rd}\n[{commit_link_str}]({commit_link})\n{l}'
    rd = f'{rd}\n{hastags}'
    return rd