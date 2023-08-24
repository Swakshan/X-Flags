from comman import old_file_name,new_file_name,channel_id,DEBUG
from comman import readJson,strpattern
from tele import sendMsg,editMsg
import sys
from urllib.parse import unquote

msg_id = sys.argv[1]

def changes():
    def getValue(config:dict):
        if "type" in config and config['type'] == "experiment":
            return "experiment"
        if "value" in config:
            return config['value']
        if "defaultValue" in config:
            return config['defaultValue']
        return ""
        
    try:
        old_features = readJson(old_file_name)
        new_features = readJson(new_file_name)

        old_features = old_features['default']
        new_features = new_features['default']

        old_features_configs = old_features['config']
        new_features_configs = new_features['config']
        
        if "debug" in old_features:
            old_features_configs_debug = old_features['debug']
            old_features_configs = {**old_features_configs,**old_features_configs_debug}

        if "debug" in new_features:
            new_features_configs_debug = new_features['debug']
            new_features_configs = {**new_features_configs,**new_features_configs_debug}

        if not new_features_configs:
            return False

        new_features_configs_2 = {}
        upd_features_configs = []
        for feat in new_features_configs:
            new_features_config_value = getValue(new_features_configs[feat])
        
            if not feat in old_features_configs:  # if new flag is not present on old flag list
                new_features_configs_2[feat] = new_features_config_value
                continue
            elif new_features_config_value != getValue(old_features_configs[feat]): # if flag has value update
                upd_features_configs.append(feat)
            old_features_configs.pop(feat)

        flag_data = {"added": new_features_configs_2,
                    "updated": upd_features_configs,
                    "removed": old_features_configs
                    }
        
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