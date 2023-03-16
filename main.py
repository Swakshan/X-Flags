import json
from pprint import pprint
import os,sys
from tele import sendMsg

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
        nf = f'• `{name}` : {value}\n{nf}'
    
    of = ""
    for f in old_flags:
        name = f
        value = old_flags[f]['value']
        of = f'• `{name}`\n{of}'

    vername = vername.replace('.','\\.').replace('-','\\-')
    nf = nf.replace('.','\\.').replace('-','\\-')
    of = of.replace('.','\\.').replace('-','\\-')

    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=split"
    l = printLine()
    rd=""

    rd = f"*⚠️{vername}⚠️*\nNo Flags updates\n{l}\n"   
    if len(nf):
        rd = f"*⚠️{vername}⚠️*\n"
        rd = f'{rd}\n__Added__'
        rd = f'{rd}\n{nf}'
        rd = f'{rd}\n{l}\n'
    rd = f'{rd}[Updated and Removed flags]({commit_link})\n{l}\n'
    # if len(of):
    #     rd = f'{rd}\n__Removed__'
    #     rd = f'{rd}\n{of}'
    #     rd = f'{rd}\n{l}\n'

    return rd


vername = sys.argv[1]
old_file_name = sys.argv[2]
flags_channel_id = "-1001977930895"
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
    sendMsg(chat_id=flags_channel_id,text=strmsg,tag=vername)