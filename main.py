import json
from pprint import pprint
import os,sys
from tele import sendMsg,editMsg

USERNAME = "Swakshan"
REPO_NAME = "Twitter-Android-Flags"
SHA = os.environ.get('GIT_COMMIT_SHA')


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
        # nf = f'• `{name}` : {value}\n{nf}'
        nf = f'• `{name}`\n{nf}'
    
    # of = ""
    # for f in old_flags:
    #     name = f
    #     value = old_flags[f]['value']
    #     of = f'• `{name}`\n{of}'

    version_name = vername
    vername = vername.replace('.','\\.').replace('-','\\-')
    nf = nf.replace('.','\\.').replace('-','\\-')
    # of = of.replace('.','\\.').replace('-','\\-')

    pin_link = f"https://t.me/c/{channel_id}/{pin_msg}"
    download_link = f'https://apkcombo.com/search/com.twitter.android/download/phone-{version_name}-apk'
    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=split"
    l = printLine()
    rd=""

    rd = f"*⚠️{vername}⚠️*\n"
    rd = f'{rd}\n[Download Link]({download_link}) \\|[Other Versions]({pin_link})\n{l}'
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


vername = sys.argv[1]
old_file_name = sys.argv[2]
msg_id = sys.argv[3]

pin_msg = "23"
channel_id = "1977930895"
flags_channel_id = "-100"+channel_id
feature_data_file_name = "dummy/feature_data.json"

old_features = readJson(old_file_name)
new_features = readJson(feature_data_file_name)

old_features_configs = old_features['default']['config']
new_features_configs = new_features['default']['config']

new_features_configs_2 = {}
for feat in new_features_configs:
    if not feat in old_features_configs:
        new_features_configs_2[feat] = new_features_configs[feat]['value']
        continue
    old_features_configs.pop(feat)


strmsg = strpattern(vername,new_features_configs_2,old_features_configs)
# print(strmsg)
if len(strmsg):
    try:
        editMsg(chat_id=flags_channel_id,msgId=msg_id,text=strmsg,tag=vername)
    except Exception as e:
        sendMsg(chat_id=flags_channel_id,text=strmsg,tag=vername)
        print(str(e))