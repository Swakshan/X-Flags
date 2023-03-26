import os,json

USERNAME = "Swakshan"
REPO_NAME = "Twitter-Android-Flags"
SHA = os.environ.get('GIT_COMMIT_SHA')
channel_id =  os.environ.get('CHANNEL_ID')#"-1001977930895"
# pin_msg =  os.environ.get('PIN_MSG')
pin_msg =  24


def printJson(data):
    print(json.dumps(data,indent=4))


def readJson(filename):
    f = open(filename)
    return json.load(f)

def printLine():
    return "*\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-*"

def strpattern(vername,new_flags,old_flags):
    
    nf = ""
    for f in new_flags:
        name = f
        value = new_flags[f]
        ty = type(value).__name__
        nf = f'• `{name}` :{ty}\n{nf}'
        # nf = f'• `{name}`\n{nf}'
    
    # of = ""
    # for f in old_flags:
    #     name = f
    #     value = old_flags[f]['value']
    #     of = f'• `{name}`\n{of}'

    version_name = vername
    vername = vername.replace('.','\\.').replace('-','\\-')
    nf = nf.replace('.','\\.').replace('-','\\-')
    # of = of.replace('.','\\.').replace('-','\\-')

    channel_id = channel_id.replace('-100','')
    pin_link = f"https://t.me/c/{channel_id}/{pin_msg}"
    download_link = f'https://apkcombo.com/search/com.twitter.android/download/phone-{version_name}-apk'
    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=unified"
    l = printLine()
    rd=""

    rd = f"*⚠️{vername}⚠️*\n"
    rd = f'{rd}\n[Download Link]({download_link}) \\| [Other Versions]({pin_link})\n{l}'
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
