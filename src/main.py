import os, shutil, sys
from constants import isDebug, getRootDir, DUMMY_FOLDER, MAIN_FOLDER,OLD_FILE_NAME,NEW_FILE_NAME
from enums import Application, ReleaseType, Platform, Source
from common import writeJson, readJson, get_exception
from processX import process as xProcess
from model import DATA
from basics import printCmd
from compare import compareFlags
import argparse

VER = "v20.1 : update apkm slug"

def flagName(data:DATA):
    os.makedirs(MAIN_FOLDER,exist_ok=True)
    
    app = data.app.value
    platform = data.platform.value
    typ = data.typ.value
    
    flagFileName = f"{app}_flags_{platform}"
    flagFileName = flagFileName if platform == Platform.WEB.value else f"{flagFileName}_{typ}"
    flagFileName +=".json"
    return getRootDir()+"/"+flagFileName

def main(data:DATA):
    flagFileName = flagName(data)
    
    # move existing/default flags to old flags
    shutil.move(flagFileName, OLD_FILE_NAME)
    
    sts = False
    app:Application = data.app
    printCmd(f"processing {app.value}")
    if app == Application.X:
        sts = xProcess(data,flagFileName)
    
    if sts:
        # new flags as default flags
        shutil.copy(NEW_FILE_NAME, flagFileName)
        
        printCmd(f"comparing flags")
        compareFlags()
    else:
        print("Status: False")
    
if not isDebug():
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-a","--app", help="App name - X/Grok")
    # parser.add_argument("-t","--type", help="Release type - Stable/Beta/Alpha")
    # parser.add_argument("-p","--platform", help="Platform - Android/iOS/Web")
    # parser.add_argument("-s","--source", help="Source - Manual/Web/apkMirror")
    # parser.add_argument("-v","--vername", help="Vername - Web/10.10-beta.1")
    # parser.add_argument("-d","--downLink", help="Download link")
    # parser.add_argument("-m","--msgId", help="Telegram message id")
    # args = parser.parse_args()
    args = sys.argv
    
    app = args[1].lower()
    plt = args[2].lower()
    src = args[3].lower()
    typ = args[4].lower()
    down_link = args[5]
    msg_id = args[6]
    vername = args[7]

    app = Application(app)
    typ = ReleaseType(typ)
    platform = Platform(plt)
    source = Source(src)
    data = DATA(vername, down_link, msg_id, source, platform, typ, app)
    print(f"DATA = {DATA}")
    main(data)
    
