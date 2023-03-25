from comman import *
from tele import sendMsg,editMsg
import sys

DUMMY_FOLDER = './dummy/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

vername = sys.argv[1]
msg_id = sys.argv[2]

old_file_name = MAIN_FOLDER+'old_feature_data.json'
new_file_name = MAIN_FOLDER+'new_feature_data.json'

def changes(vername):
    old_features = readJson(old_file_name)
    new_features = readJson(new_file_name)

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
            editMsg(chat_id=channel_id,msgId=msg_id,txt=strmsg)
        except Exception as e:
            sendMsg(chat_id=channel_id,text=strmsg,tag=vername)
            print(str(e))

changes(vername)