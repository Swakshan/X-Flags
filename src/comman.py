import os,json
from enum import Enum
# from dotenv import load_dotenv
# load_dotenv()


def getEnv(key):
    return os.environ.get(key)

DEBUG  =  0

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

def printLine():
    return "*--------------*"

def commitLinkFormat(flag_data):
    def countFormat(count):
        if not count:
            return False
        
        f = "Flags" if count>1 else "Flag"
        return f"{count} {f}"
    
    msg = ""
    for func in ('added','updated','removed'):
        flags = flag_data[func]
        fStr = countFormat(len(flags))
        if fStr:
            msg = f"{msg} and {fStr} {func.title()}"
    
    msg = msg[5:] if len(msg) else "Repo Link"
    return msg

def strpattern(flag_data,flag_data_2):
    manifest_file = readJson(manifest_file_name)
    vername = manifest_file['version_name']
    vercode = manifest_file['vercode']
    down_link = manifest_file['download_link']
    hash_value = manifest_file['hash']
    platform = manifest_file['os']
    
    nf = ""
    new_flags = dict(list(flag_data['added'].items())[:NEW_FLAG_LIMIT])
    for f in new_flags:
        name = f
        value = new_flags[f]
        ty = type(value).__name__ if value!="experiment" else "exp"
        nf = f'• `{name}` :{ty}\n{nf}'

    commit_link_str = commitLinkFormat(flag_data)
    commit_link_str_2 = False
    pin_link = f"https://t.me/c/{CHANNEL_ID}/{PIN_MSG}"
    platformRow = f"_Platform_: `{platform.title()}`"
    vercode_str = ""
    if platform.lower() == Platform.ANDROID.value:
        vercode_str = f"__Vercode__:\n`{vercode}`" if int(vercode) else vercode_str #if not "0"
        ps_link = 'https://play.google.com/store/apps/details?id='+PKG_NAME
        apkc_link = f'https://apkcombo.com/search/{PKG_NAME}/download/phone-{vername}-apk'
        apkf_link = f'https://apkflash.com/apk/app/{PKG_NAME}/twitter/download/{vername}'

        apkm_vername = vername.replace('.','-')
        apkm_link = f'https://www.apkmirror.com/apk/x-corp/x/twitter-{apkm_vername}-release/'

        linkRow = f'[Play Store]({ps_link}) | [APKMirror]({apkm_link})\n[APKCombo]({apkc_link}) | [APKFlash]({apkf_link})\n'
        if down_link:
            linkRow = f'[Aptoide]({down_link})\n{linkRow}*\\[⚠️APK from Aptoide is known for crashes⚠️\\]*\n'
                
    elif platform.lower() == Platform.WEB.value:
        vername = vername.title()
        vercode_str = f"__Hash__:\n`{hash_value}`"
        linkRow = f"[Web Link]({WEB_LINK})\n"

    elif platform.lower() == Platform.IOS.value:
        platformRow = f"_Platform_: `{platform.upper()}`"
        linkRow = f"[App Store]({APP_STORE_LINK})\n"
        if flag_data_2:
            commit_link_str_2 = commitLinkFormat(flag_data_2)

    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=split"
    l = printLine()
    # rd = f"⚠️`{vername}`⚠️\n\n{platformRow}\n"
    rd = f"⚠️`{vername}`⚠️\n"
    rd = rd if not len(vercode_str) else f"{rd}{vercode_str}\n"
    rd = f'{rd}\n{linkRow}\n[Other Version Details]({pin_link})\n{l}'
    if len(nf):
        rd = f'{rd}\n__Flags Added__'
        rd = f'{rd}\n{nf}\n{l}'
    else:
         rd = f"{rd}\nNo New Flags\n{l}"
    rd = f'{rd}\n[{commit_link_str}]({commit_link})\n{l}'
    if commit_link_str_2:
        rd = f'{rd}\n_iPad:_\n[{commit_link_str_2}]({commit_link})\n{l}'
    return rd