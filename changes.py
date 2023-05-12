from comman import old_file_name,new_file_name,channel_id,DEBUG
from comman import readJson,strpattern
from tele import sendMsg,editMsg
import sys
from urllib.parse import unquote

msg_id = sys.argv[1]

def changes():
    try:
        old_features = readJson(old_file_name)
        new_features = readJson(new_file_name)

        old_features_configs = old_features['default']['config']
        new_features_configs = new_features['default']['config']

        if not new_features_configs:
            return False

        new_features_configs_2 = {}
        upd_features_configs = []
        for feat in new_features_configs:
            new_features_config_value = new_features_configs[feat]['value']
        
            if not feat in old_features_configs:  # if new flag is not present on old flag list
                new_features_configs_2[feat] = new_features_config_value
                continue
            elif new_features_config_value != old_features_configs[feat]['value']: # if flag has value update
                upd_features_configs.append(feat)
            old_features_configs.pop(feat)

        flag_data = {"added": new_features_configs_2,
                        "updated": upd_features_configs,
                        "removed": old_features_configs}

        strmsg = strpattern(flag_data)
        if DEBUG:
            return strmsg
        ch_id = "-100"+channel_id
        if len(strmsg):
            try:
                editMsg(chat_id=ch_id,msgId=msg_id,txt=strmsg)
            except Exception as e:
                sendMsg(chat_id=ch_id,text=strmsg,tag='')
                print(str(e))
    except Exception as e:
        print(str(e))
        return False

changes()