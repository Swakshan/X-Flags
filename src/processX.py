import requests, json, os, shutil, sys
from tqdm import tqdm
from pprint import pprint
from constants import (
    DUMMY_FOLDER,
    MAIN_FOLDER,
    NEW_FILE_NAME,
    OLD_FILE_NAME,
    MANIFEST_FILE_NAME, getEnv,getRootDir
)
from basics import writeJson, readJson, get_exception
from enums import Source, Platform, ReleaseType, Application
from common import downloader,downloadAndroid,pairipDetector,unzipper
from model import DATA
from appData import webfeatureSwitches

def process(data:DATA,flagFileName:str):
    sts = False
    try:
        isPairip = data.pairip
        app = data.app
        typ = data.typ
        platform = data.platform
        source = data.src
        down_link = data.link
        

        if platform == Platform.WEB:
            vername = data.vername
            sha, hash = vername.split("||")
            fs = webfeatureSwitches(hash)
            # create the flags in existing flags
            writeJson(flagFileName, fs)
            writeJson(NEW_FILE_NAME,fs)
            sts = True

        elif platform == Platform.IOS:
            if ".json" in down_link:
                downloader(url=down_link, filePath=NEW_FILE_NAME, isJson=True)
                
            else:
                downloader(down_link)
                s = unzipper(platform)
                
                if not s:
                    raise Exception("Error unzipping")
            sts = True

        elif platform == Platform.ANDROID:
            downloadAndroid(down_link,source)

            s = unzipper(platform)
            if not s:
                raise Exception("Error unzipping")

            isPairip = pairipDetector()
            sts = True

        data.pairip = isPairip

    except Exception as e:
        print(get_exception())
    
    d = data.toJSON()
    d["sts"]=sts
    writeJson(MANIFEST_FILE_NAME, d)
    return sts