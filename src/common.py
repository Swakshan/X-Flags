from enums import Source, Platform, ReleaseType

from constants import (ZIP_FILE, EXTRACT_FOLDER, PKG_NAME, NEW_FILE_NAME,
                       headers, getEnv)
from basics import get_exception, readJson, writeJson,printSubCmd
import requests
import zipfile
import os
import shutil
from apkutils import APK
from tqdm import tqdm
from appData import apkM,apkCombo,

def downloader(url, filePath=ZIP_FILE, isJson=False):
    if os.path.exists(filePath):
        printSubCmd(f"{filePath} exists" , "!")
        return True
    response = requests.get(url, stream=True, headers=headers())
    if not isJson:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB',
                            unit_scale=True)

        with open(filePath, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    else:
        js = response.json()
        writeJson(filePath, js)

def downloadAndroid(url, source):
    down_link = None
    if source == Source.APKM:
        down_link = apkM(url)

    elif source == Source.APKC:
        down_link = apkCombo(url)

    elif source == Source.APT or source == Source.APKP or Source.MAN:
        down_link = url

    else:
        raise Exception(f"Error: Source not found + {source.value}")
    printSubCmd("Downloading " + down_link + " from: " + source.value)
    downloader(url=down_link)

def unzipper(platform):
    def extract(src, new_name):
        zip_obj.extract(src, path=EXTRACT_FOLDER)
        fg = readJson(EXTRACT_FOLDER + src)
        writeJson(new_name, fg)
        return True
    feature_file = False
    zip_obj = zipfile.ZipFile(ZIP_FILE, "r")
    file_list = zip_obj.namelist()
    
    if platform == Platform.ANDROID:
        FLAG_FOLDER = "res/raw"
        FLAG_FILE = f"{FLAG_FOLDER}/feature_switch_manifest"
        apk_name_1 = f"{PKG_NAME}.apk"
        apk_name_2 = f"base.apk"
        
        if apk_name_1 in file_list or apk_name_2 in file_list:
            apk_name = apk_name_2 if apk_name_2 in file_list else apk_name_1
            # Needed to change the name of the apk for pairip detection
            temp_path = zip_obj.extract(apk_name, path=EXTRACT_FOLDER)
            new_path = f"{EXTRACT_FOLDER}app.apk"
            shutil.move(temp_path, new_path)
            zip_obj = zipfile.ZipFile(new_path, "r")
            feature_file = True

        elif FLAG_FILE in file_list:
            feature_file = True

        if feature_file:
            return extract(FLAG_FILE, NEW_FILE_NAME)

    elif platform == Platform.IOS:
        FLAG_FOLDER = "Payload/Twitter.app"
        f1 = False
        f2 = False
        
        FLAG_FILE = f"{FLAG_FOLDER}/fs_embedded_defaults_production.json"
        if FLAG_FILE in file_list:
            f1 = extract(FLAG_FILE, NEW_FILE_NAME)
            
        FLAG_FILE = f"{FLAG_FOLDER}/fs_embedded_defaults_ipad_production.json"
        if FLAG_FILE in file_list:
            f2 = extract(FLAG_FILE, NEW_FILE_NAME+"_2")
        
        return f1 & f2
        
    return False

def pairipDetector():
    printSubCmd("Detecting Paririp")
    apkPath = ZIP_FILE
    xapkPath = f"{EXTRACT_FOLDER}app.apk"
    if os.path.exists(xapkPath):
        apkPath = xapkPath

    apk = APK.from_file(apkPath)
    manifest = apk.get_manifest()
    
    if "com.pairip.application.Application" in manifest:
        return True
    return False