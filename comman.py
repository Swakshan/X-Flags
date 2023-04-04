import os,json

USERNAME = "Swakshan"
REPO_NAME = "Twitter-Android-Flags"
SHA = os.environ.get('GIT_COMMIT_SHA')
channel_id =  os.environ.get('CHANNEL_ID')#"-1001977930895"
pin_msg =  os.environ.get('PIN_MSG')
# pin_msg =  24
DUMMY_FOLDER = './dummy/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

def printJson(data):
    print(json.dumps(data,indent=4))


def readJson(filename):
    f = open(filename,'r')
    d = json.load(f)
    f.close()
    return d

def printLine():
    return "*\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-*"

def strpattern(new_flags,old_flags):
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
    
    apkc_link = f'https://apkcombo.com/search/com.twitter.android/download/phone-{vername}-apk'
    apkm_vername = vername.replace('.','-')
    apkm_link = f'https://www.apkmirror.com/apk/twitter-inc/twitter/twitter-{apkm_vername}-release/'
    linkRow = f'[ApkCombo]({apkc_link}) \\| [APKMirror]({apkm_link})\n'
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
