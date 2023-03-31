import requests
import json
import os
import shutil
import sys
from appData import ApkCombo, Aptiode
from tqdm import tqdm
import zipfile
from pprint import pprint


typ = sys.argv[1]
source = sys.argv[2]


DUMMY_FOLDER = './dummy/'
ZIP_FILE = DUMMY_FOLDER+'app.zip'

EXTRACT_FOLDER = DUMMY_FOLDER+'Extracted/'
MAIN_FOLDER = DUMMY_FOLDER+'main/'

old_file_name = MAIN_FOLDER+'old_feature_data.json'
new_file_name = MAIN_FOLDER+'new_feature_data.json'

if os.path.exists(DUMMY_FOLDER):
    shutil.rmtree(DUMMY_FOLDER)
os.makedirs(MAIN_FOLDER)


def downloader(url):
    response = requests.get(url, stream=True)

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(ZIP_FILE, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()


def unzipper():
    try:
        feature_file = False
        zip_obj = zipfile.ZipFile(ZIP_FILE, 'r')
        file_list = zip_obj.namelist()
        if "com.twitter.android.apk" in file_list:
            zip_obj.extract("com.twitter.android.apk", path=EXTRACT_FOLDER)
            zip_obj = zipfile.ZipFile(
                EXTRACT_FOLDER+"com.twitter.android.apk", 'r')
            feature_file = True

        elif "res/raw/feature_switch_manifest" in file_list:
            feature_file = True

        if feature_file:
            zip_obj.extract("res/raw/feature_switch_manifest",
                            path=EXTRACT_FOLDER)
            os.rename(EXTRACT_FOLDER +
                      'res/raw/feature_switch_manifest', new_file_name)
            return True
    except Exception as e:
        print(str(e))

    return False


def downTwt(typ):
    appName = "Twitter"
    try:
        app = "com.twitter.android"
        prinData = ""

        # if ("apkcombo.com" or 'apkcombo-com' in downLink) and not rd['status']: #sts is false and downlink has apkcombo
        apkC = ApkCombo(pkgName=app)
        l = apkC.versions()
        # pprint(l)
        if l['status']:
            data = l['data']
            ty = data[typ.lower()]
            typ = ty['vername']
            l = apkC.getApk(typ, "xapk")
            if l['status']:
                d = l['data']
                downLink = d['link']
                fileName = f"{typ}.{d['apktype']}"
                print(f"Downloading: {fileName}")
                downloader(downLink)
                # pprint(d)
                return typ,downLink
            else:
                prinData = "version not Found"
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(str(e))
    return False


def downTwt2(typ):
    appName = "Twitter"
    try:
        app = "com.twitter.android"
        prinData = ""

        apt = Aptiode(pkgName=app)
        l = apt.versions()
        # pprint(l)
        if l['status']:
            data = l['data']
            ty = data[typ.lower()]
            typ = ty['vername']
            downLink = ty['link']
            fileName = f"{typ}.{ty['apk-type']}"
            print(f"Downloading: {fileName}")
            downloader(downLink)
            return typ,downLink
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(str(e))
    return False


def main(typ):
    try:
        typ = typ.lower()
        version_number = False
        downLink = ""
        if source == "apt":
            version_number,downLink = downTwt2(typ)
        else:
            version_number,downLink = downTwt(typ)
            downLink = False # if apkcombo dont save the link
        if not version_number:
            return False

        existsing_flag_file = f'flags_{typ}.json'
        shutil.copyfile(existsing_flag_file, MAIN_FOLDER +
                        'old_feature_data.json')

        s = unzipper()
        if not s:
            return False
        os.remove(existsing_flag_file)
        shutil.copy(new_file_name, existsing_flag_file)

        f = open('manifest.json', 'w')
        d = {'version_name': version_number,'download_link':downLink}
        f.write(json.dumps(d))
        f.close()

        return True
    except Exception as e:
        print(str(e))

    return False


s = main(typ)
print(s)
