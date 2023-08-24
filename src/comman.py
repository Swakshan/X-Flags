import os,json

DEBUG  =  0

APP_NAME = "Twitter"
PKG_NAME = 'com.twitter.android'
DUMMY_FOLDER = './dummy/'
ZIP_FILE = DUMMY_FOLDER+'app.zip'

EXTRACT_FOLDER = DUMMY_FOLDER+'Extracted/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

old_file_name = MAIN_FOLDER+'old_feature_data.json'
new_file_name = MAIN_FOLDER+'new_feature_data.json'
manifest_file_name = "manifest.json"
NEW_FLAG_LIMIT = 25

USERNAME = "Swakshan"
REPO_NAME = "X-Flags"
SHA = os.environ.get('GIT_COMMIT_SHA')
channel_id =  os.environ.get('CHANNEL_ID')
pin_msg =  os.environ.get('PIN_MSG')


WEB_LINK = 'https://twitter.com/'
M_WEB_LINK = 'https://m.twitter.com/'
TWT_SW_URL = f"{WEB_LINK}sw.js"

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
    for func in ('added','removed','updated'):
        flags = flag_data[func]
        fStr = countFormat(len(flags))
        if fStr:
            msg = f"{msg} and {fStr} {func.title()}"
    
    msg = msg[5:] if len(msg) else "Repo Link"
    return msg

def strpattern(flag_data):
    manifest_file = readJson(manifest_file_name)
    vername = manifest_file['version_name']
    vercode = manifest_file['vercode']
    down_link = manifest_file['download_link']
    hash_value = manifest_file['hash']

    
    nf = ""
    new_flags = dict(list(flag_data['added'].items())[:NEW_FLAG_LIMIT])
    for f in new_flags:
        name = f
        value = new_flags[f]
        ty = type(value).__name__ if value!="experiment" else "exp"
        nf = f'• `{name}` :{ty}\n{nf}'

    commit_link_str = commitLinkFormat(flag_data)
    pin_link = f"https://t.me/c/{channel_id}/{pin_msg}"
    
    ps_link = 'https://play.google.com/store/apps/details?id='+PKG_NAME
    apkc_link = f'https://apkcombo.com/search/{PKG_NAME}/download/phone-{vername}-apk'
    apkf_link = f'https://apkflash.com/apk/app/{PKG_NAME}/twitter/download/{vername}'

    apkm_vername = vername.replace('.','-')
    apkm_link = f'https://www.apkmirror.com/apk/x-corp/x/twitter-{apkm_vername}-release/'

    linkRow = f'[Play Store]({ps_link}) | [APKMirror]({apkm_link})\n[APKCombo]({apkc_link}) | [APKFlash]({apkf_link})\n'
    if down_link:
        linkRow = f'[Aptoide]({down_link})\n{linkRow}*\\[⚠️APK from Aptoide is known for crashes⚠️\\]*\n.'

    vercode_str = f"__vercode__:\n`{vercode}`"
    if vername=="web":
        linkRow = f"[Web Link]({WEB_LINK})\n"
        vername = vername.title()
        vercode_str = f"__hash__:\n`{hash_value}`"
    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=unified"
    l = printLine()
    rd = f"⚠️`{vername}`⚠️\n{vercode_str}\n"
    rd = f'{rd}\n{linkRow}\n[Other Version Details]({pin_link})\n{l}'
    if len(nf):
        rd = f'{rd}\n__Flags Added__'
        rd = f'{rd}\n{nf}\n{l}'
    else:
         rd = f"{rd}\nNo New Flags\n{l}"
    rd = f'{rd}\n[{commit_link_str}]({commit_link})\n{l}\n'
    return rd