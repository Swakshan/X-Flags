import os,json

PKG_NAME = 'com.twitter.android'
DUMMY_FOLDER = './dummy/'
ZIP_FILE = DUMMY_FOLDER+'app.zip'

EXTRACT_FOLDER = DUMMY_FOLDER+'Extracted/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

old_file_name = MAIN_FOLDER+'old_feature_data.json'
new_file_name = MAIN_FOLDER+'new_feature_data.json'


USERNAME = "Swakshan"
REPO_NAME = "Twitter-Android-Flags"
SHA = os.environ.get('GIT_COMMIT_SHA')
channel_id =  os.environ.get('CHANNEL_ID')
pin_msg =  os.environ.get('PIN_MSG')

def printJson(data):
    print(json.dumps(data,indent=4))


def readJson(filename):
    f = open(filename,'r')
    d = json.load(f)
    f.close()
    return d

def printLine():
    return "*\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-*"

def strpattern(new_flags):
    manifest_file = readJson('manifest.json')
    vername = manifest_file['version_name']
    down_link = manifest_file['download_link']
    nf = ""
    for f in new_flags:
        name = f
        value = new_flags[f]
        ty = type(value).__name__
        nf = f'• `{name}` :{ty}\n{nf}'
    vername = vername.replace('.','\\.').replace('-','\\-')
    nf = nf.replace('.','\\.').replace('-','\\-')
    # of = of.replace('.','\\.').replace('-','\\-')

    pin_link = f"https://t.me/c/{channel_id}/{pin_msg}"
    
    ps_link = 'https://play.google.com/store/apps/details?id='+PKG_NAME
    apkc_link = f'https://apkcombo.com/search/{PKG_NAME}/download/phone-{vername}-apk'
    apkm_vername = vername.replace('.','-')
    apkm_link = f'https://www.apkmirror.com/apk/twitter-inc/twitter/twitter-{apkm_vername}-release/'
    linkRow = f'[Play Store]({ps_link})\n[ApkCombo]({apkc_link}) \\| [APKMirror]({apkm_link})\n'
    if down_link:
        linkRow = f'[Aptiode]({down_link}) \\| {linkRow}'
    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=unified"
    l = printLine()
    rd=""

    rd = f"*⚠️{vername}⚠️*\n"
    rd = f'{rd}\n{linkRow}\n[Other Version Details]({pin_link})\n{l}'
    if len(nf):
        rd = f'{rd}\n__Flags Added__'
        rd = f'{rd}\n{nf}\n{l}'
    else:
         rd = f"{rd}\nNo New Flags\n{l}"
    rd = f'{rd}\n[Updated and Removed flags]({commit_link})\n{l}\n'
    
    
    # if len(of):
    #     rd = f'{rd}\n__Removed__'
    #     rd = f'{rd}\n{of}'
    #     rd = f'{rd}\n{l}\n'

    return rd
