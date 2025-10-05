import os, shutil, sys
from constants import isDebug, getRootDir, DUMMY_FOLDER, MAIN_FOLDER,OLD_FILE_NAME,NEW_FILE_NAME
from enums import Application, ReleaseType, Platform, Source
from common import writeJson, readJson, get_exception
from processX import process as xProcess
from model import DATA
from basics import printCmd
from compare import compareFlags
import argparse

VER = "v20 : updated ReadMe"

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
    
    app:Application = data.app
    printCmd(f" processing {app.value}")
    if app == Application.X:
        xProcess(data,flagFileName)
        
    # new flags as default flags
    shutil.copy(NEW_FILE_NAME, flagFileName)
    
    printCmd(f" comparing flags")
    compareFlags()
    
if not isDebug():
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="App name - X/Grok",required=True)
    parser.add_argument("type", help="Release type - Stable/Beta/Alpha")
    parser.add_argument("platform", help="Platform - Android/iOS/Web",required=True)
    parser.add_argument("source", help="Source - Manual/Web/apkMirror",required=True)
    parser.add_argument("vername", help="Vername - Web/10.10-beta.1",required=True)
    parser.add_argument("downLink", help="Download link",required=True)
    parser.add_argument("msgId", help="Telegram message id")
    args = parser.parse_args()
       
    app = args.app.lower()
    typ = args.type.lower()
    plt = args.platform.lower()
    src = args.source.lower()
    vername = args.vername
    down_link = args.downLink
    msg_id = args.msgId

    app = Application(app)
    typ = ReleaseType(typ)
    platform = Platform(plt)
    source = Source(src)
    data = DATA(vername, down_link, msg_id, source, platform, typ, app)
    
    main(data)
