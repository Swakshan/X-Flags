from comman import old_file_name,new_file_name,CHANNEL_ID,DEBUG,new_file_ipad_name,old_file_ipad_name
from comman import readJson,strpattern
from tele import sendMsg,editMsg
import sys,os
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
    
    def flagChanges(old_file_name,new_file_name):
        old_features = readJson(old_file_name)
        new_features = readJson(new_file_name)

        if "default" in new_features:
            old_features = old_features['default']
            new_features = new_features['default']

        old_features_configs = old_features['config']
        new_features_configs = new_features['config']
        
        old_features_configs_debug = {}
        new_features_configs_debug = {}
        if "debug" in old_features:
            old_features_configs_debug = old_features['debug']
            new_features_configs_debug = new_features['debug']

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

        
        debug_features_config = []
        if len(new_features_configs_debug):
            for feat in new_features_configs_debug:
                if feat in old_features_configs_debug:
                    continue
                if feat in upd_features_configs or feat in new_features_configs_2:
                    continue
                
                debug_features_config.append(feat)



        return {"added": new_features_configs_2,
                "debug": debug_features_config,
                "updated": upd_features_configs,
                "removed": old_features_configs
                }  
    try:
        flag_data_2 = False
        flag_data = flagChanges(old_file_name,new_file_name)
        if not flag_data:
            return False

        if os.path.exists(new_file_ipad_name):
            flag_data_2 = flagChanges(old_file_ipad_name,new_file_ipad_name)
        
        strmsg = strpattern(flag_data,flag_data_2)
        ch_id = "-100"+CHANNEL_ID
        if DEBUG:
            print(strmsg)
            # return strmsg
            return True
        if len(strmsg):
            try:
                if int(msg_id):
                    editMsg(chat_id=ch_id,msgId=msg_id,txt=strmsg)
                else:
                    sendMsg(chat_id=ch_id,text=strmsg)
            except Exception as e:
                sendMsg(chat_id=ch_id,text=strmsg)
                print(str(e))
    except Exception as e:
        print(str(e))
        return False

changes()