import os, shutil, sys
from constants import isDebug, getRootDir, DUMMY_FOLDER, MAIN_FOLDER,OLD_FILE_NAME,NEW_FILE_NAME
from enums import Application, ReleaseType, Platform, Source
from common import writeJson, readJson, get_exception
from processX import process as xProcess
from model import DATA
from basics import printCmd
from compare import compareFlags
import argparse

VER = "v22.12 : update readMe"

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
    plt:Platform = data.platform
    
    printCmd(f"processing {app.value}")
    if app == Application.X:
        if plt == Platform.IOS:
            # move existing/default ipad flags to old flags
            shutil.move(flagFileName.replace("ios","ipad"), OLD_FILE_NAME+"_2")
            
        sts = xProcess(data,flagFileName)
    
    if sts:
        # new flags as default flags
        shutil.copy(NEW_FILE_NAME, flagFileName)
        if plt == Platform.IOS and app == Application.X:
            shutil.copy(NEW_FILE_NAME+"_2",flagFileName.replace("ios","ipad"))
        
        printCmd(f"comparing flags")
        compareFlags()
    else:
        print("Status: False")
    
if not isDebug():
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    args = sys.argv

    app = args[1].lower()
    plt = args[2].lower()
    src = args[3].lower()
    typ = args[4].lower()
    msg_id = args[5]
    vername = args[6]
    vercode = args[7]
    down_link = args[8]

    app = Application(app)
    typ = ReleaseType(typ)
    platform = Platform(plt)
    source = Source(src.strip())
    data:DATA = DATA(vername, down_link, msg_id, source, platform, typ, app,vercode)

    main(data)
    
