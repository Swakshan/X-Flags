from constants import OLD_FILE_NAME,NEW_FILE_NAME,CHANGES_FILE_NAME,MANIFEST_FILE_NAME,USERNAME,REPO_NAME,NEW_FLAG_LIMIT,getEnv
from enums import Platform,Application
from model import DATA
from basics import writeJson,readJson,printSubCmd
import os

def compareFlags():
    def getValue(config:dict):
        if "type" in config and config['type'] == "experiment":
            return "experiment"
        if "value" in config:
            return config['value']
        if "defaultValue" in config:
            return config['defaultValue']
        return ""
    
    def createChangesFile(data:DATA,new_file_name,old_file_name,changes_file_name):
        old_file = readJson(old_file_name)
        new_file = readJson(new_file_name)
        
        new_flags = {}
        old_flags = {}
        new_debug_flags = {}
        old_debug_flags = {}
        
        if data.app in [Application.X,Application.XLITE]:
            if data.platform == Platform.WEB:
                new_flags = new_file['config']
                old_flags = old_file['config']
                
                new_debug_flags = list(new_file['debug'].keys())
                old_debug_flags = list(old_file['debug'].keys())
            else:
                new_flags = new_file['default']['config']
                old_flags = old_file['default']['config']
                if data.platform == Platform.ANDROID:
                    new_debug_flags = new_file['experiment_names']
                    old_debug_flags = old_file['experiment_names']
            
        
        old_flags_copy = old_flags.copy()
        old_debug_flags_copy = old_debug_flags.copy()
        
        FLAGS = {'added':{},'updated':0,'removed':0}
        for flag in new_flags:
            flag_value = getValue(new_flags[flag])
            
            if flag not in old_flags: # If the flag is present in new but not in old.
                FLAGS['added'][flag] = type(flag_value).__name__
                
            else: # If the flag is present in old check if removed or updated.
                if flag_value != getValue(old_flags[flag]): # If the flag value is updated.
                    FLAGS['updated']+=1
                old_flags_copy.pop(flag) # Remove that flag from old flags to calculate removed flags
        
        FLAGS['removed'] = len(old_flags_copy)
        
        DEBUG_FLAGS = {'added':[],'removed':0}
        for flag in new_debug_flags:
            if flag not in old_debug_flags:
                DEBUG_FLAGS['added'].append(flag)
            else:
                old_debug_flags_copy.remove(flag)
        DEBUG_FLAGS['removed'] = len(old_debug_flags_copy)
        
        CHANGES = {'flags':FLAGS,'debug_flags':DEBUG_FLAGS}
        
        writeJson(changes_file_name,CHANGES)
        
    manifest = readJson(MANIFEST_FILE_NAME)
    if not manifest['sts']:
        raise Exception("Status is false so skipping change compare")
    
    data:DATA = DATA.fromJSON(manifest)
    
    createChangesFile(data,NEW_FILE_NAME,OLD_FILE_NAME,CHANGES_FILE_NAME)
    
    ipadFileNameExt =  "_2"
    if os.path.exists(OLD_FILE_NAME+ipadFileNameExt):
        createChangesFile(data,NEW_FILE_NAME+ipadFileNameExt,OLD_FILE_NAME+ipadFileNameExt,CHANGES_FILE_NAME+ipadFileNameExt)
        


def commitLinkFormat(flag_data,include_added=False):
    def countFormat(count, ns="Flags"):
        if not count:
            return False

        f = ns if count > 1 else ns[:-1]
        return f"{count} {f}"

    # include added flags for X ipad
    new_flag_limit = -1 if include_added else NEW_FLAG_LIMIT
    
    msg = ""
    for key in flag_data:
        flag_det = flag_data[key]
        ns = key.title().replace("_", " ")
        for func in flag_det:
            c = 0
            if func == "added":
                c = len(flag_det['added'])
                if c < new_flag_limit :
                    continue
            else:
                c = flag_det[func]
            
            fStr = countFormat(c, ns)
            if fStr:
                msg = f"{msg} and {fStr} {func.title()}"
    msg = msg[5:] if len(msg) else "Repo Link"
    return msg


def flagMessage(data:DATA):
    printSubCmd("forming Telegram flag message")
    SHA = getEnv("GIT_COMMIT_SHA")
    flag_details = readJson(CHANGES_FILE_NAME)
    
    l = "--------------"
    nf = ""
    df = ""
    flag_data = flag_details["flags"]
    added_flags = flag_data["added"].items()
    new_flags = dict(list(added_flags)[:NEW_FLAG_LIMIT])
    for f in new_flags:
        ty = new_flags[f]
        nf = f"• `{f}` :{ty}\n{nf}"
    nfC = len(new_flags)

    debug_flag_data = flag_details["debug_flags"]
    debug_added_flags = debug_flag_data["added"]
    debug_flags = debug_added_flags[:NEW_FLAG_LIMIT]
    for f in debug_flags:
        df = f"• `{f}`\n{df}"
    dfC = len(debug_flags)

    commit_link = f"https://github.com/{USERNAME}/{REPO_NAME}/commit/{SHA}?diff=split"
    commit_link_str = commitLinkFormat(flag_details)
    rd = ""
    if nfC:
        rd = f"{rd}\n__New Flags__"
        rd = f"{rd}\n{nf}"
        rd = f"{rd}\nAnd more..." if len(added_flags) > NEW_FLAG_LIMIT else rd
        rd = f"{rd}\n{l}"
    if dfC:
        rd = f"{rd}\n__New Debug Flags__"
        rd = f"{rd}\n{df}"
        rd = f"{rd}\nAnd more..." if len(debug_added_flags) > NEW_FLAG_LIMIT else rd
        rd = f"{rd}\n{l}"
        
    elif not nfC and not dfC:
        rd = f"{rd}\nNo New Flags\n{l}"
        
    if data.platform == Platform.IOS and data.app == Application.X:
        rd = f"{rd}\n__iPhone__:\n[{commit_link_str}]({commit_link})"
        
        flag_details = readJson(CHANGES_FILE_NAME+"_2")
        commit_link_str = commitLinkFormat(flag_details,True)
        rd = f"{rd}\n__iPad__:\n[{commit_link_str}]({commit_link})"
    else:
        rd = f"{rd}\n[{commit_link_str}]({commit_link})"
    return rd