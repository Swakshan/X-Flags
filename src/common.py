import os,json
from enum import Enum
from sys import exc_info
from traceback import format_exception
from dotenv import load_dotenv
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

class Platform(Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

class Releases(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"
    WEB = "web"

def get_exception():
    etype, value, tb = exc_info()
    info, error = format_exception(etype, value, tb)[-2:]
    return f'Exception in: {info}: {error}'

def printJson(data):
    print(json.dumps(data,indent=4))

def writeJson(fileName,data):
    f = open(fileName, 'w')
    json.dump(data,f,indent=4)
    f.close()

def readJson(filename):
    f = open(filename,'r')
    d = json.load(f)
    f.close()
    return d

def readFile(filename):
    f = open(filename,'r',encoding='utf-8')
    d = f.read()
    f.close()
    return d

def printLine():
    return "*--------------*"

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
    platform = manifest_file['os']
    
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
    platformRow = f"_Platform_: `{platform.title()}`"
    vercode_str = ""
    if platform.lower() == Platform.ANDROID.value:
        vercode_str = f"__Vercode__:\n`{vercode}`" if int(vercode) else vercode_str #if not "0"
        ps_link = 'https://play.google.com/store/apps/details?id='+PKG_NAME
        apkc_link = f'https://apkcombo.com/search/{PKG_NAME}/download/phone-{vername}-apk'
        apkf_link = f'https://apkflash.com/apk/app/{PKG_NAME}/twitter/download/{vername}'
        apkp_link = f'https://d.apkpure.com/b/APK/{PKG_NAME}?versionCode={vercode}'
        apkm_vername = vername.replace('.','-')
        apkm_link = f'https://www.apkmirror.com/apk/x-corp/x/twitter-{apkm_vername}-release/'

        linkRowFormer("Play Store",ps_link)
        linkRowFormer("APKMirror",apkm_link)
        linkRowFormer("APKCombo",apkc_link)
        linkRowFormer("APKFlash",apkf_link)
        # linkRow = f'[Play Store]({ps_link}) | [APKMirror]({apkm_link})\n[APKCombo]({apkc_link}) | [APKFlash]({apkf_link})\n'
        if "release" in vername:
            linkRowFormer("APKPure",apkp_link)
        if down_link:
            linkRowFormer("Aptoide",down_link)
            linkRow = f'{linkRow}\n*\\[⚠️APK from Aptoide is known for crashes⚠️\\]*\n'
        
        linkRow = linkRow+"\n" if linkRow[-2]=="|" else linkRow

                
    elif platform.lower() == Platform.WEB.value:
        vername = vername.title()
        vercode_str = f"__Hash__:\n`{hash_value}`"
        linkRow = f"[Web Link]({WEB_LINK})\n"

    elif platform.lower() == Platform.IOS.value:
        platformRow = f"_Platform_: `{platform.upper()}`"
        linkRow = f"[App Store]({APP_STORE_LINK})\n"
        if flag_details_2:
            commit_link_str_2 = commitLinkFormat(flag_details_2)

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
    return rd