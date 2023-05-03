import requests,json,os,shutil,sys,zipfile
from appData import ApkCombo, Aptiode,TwtWeb
from tqdm import tqdm
from pprint import pprint
from comman import DUMMY_FOLDER,MAIN_FOLDER,ZIP_FILE,EXTRACT_FOLDER,PKG_NAME,APP_NAME,new_file_name,old_file_name,DEBUG,manifest_file_name

VER = "v4.5 : formatted commit text"


typ="web"
source="web"
if not DEBUG:
    typ = sys.argv[1]
    source = sys.argv[2]


if os.path.exists(DUMMY_FOLDER):
    shutil.rmtree(DUMMY_FOLDER)
os.makedirs(MAIN_FOLDER)

def makeJsonFile(fileName,data):
    f = open(fileName, 'w')
    f.write(json.dumps(data,indent=4))
    f.close()

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
        apk_name = f'{PKG_NAME}.apk'
        if apk_name in file_list:
            zip_obj.extract(apk_name, path=EXTRACT_FOLDER)
            zip_obj = zipfile.ZipFile(
                EXTRACT_FOLDER+apk_name, 'r')
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
    try:
        prinData = ""
        apkC = ApkCombo(pkgName=PKG_NAME)
        l = apkC.versions()
        # pprint(l)
        if l['status']:
            data = l['data']
            ty = data[typ.lower()]
            
            vername = ty['vername']
            l = apkC.getApk(vername, "xapk")
            if l['status']:
                d = l['data']
                vercode = d['vercode']
                downLink = d['link']
                fileName = f"{vername}.{d['apktype']}"
                print(f"Downloading: {fileName}")
                downloader(downLink)
                return [vername,vercode,False]# if apkcombo dont save the link
            else:
                prinData = "version not Found"
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(str(e))
    return False


def downTwt2(typ):
    try:
        prinData = ""

        apt = Aptiode(pkgName=PKG_NAME)
        l = apt.versions()
        # pprint(l)
        if l['status']:
            data = l['data']
            ty = data[typ.lower()]
            vername = ty['vername']
            vercode = ty['vercode']
            downLink = ty['link']
            fileName = f"{vername}.{ty['apk-type']}"
            print(f"Downloading: {fileName}")
            downloader(downLink)
            return [vername,vercode,downLink]
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(str(e))
    return False


def main(typ):
    try:
        hash_value = False
        typ = typ.lower()
        down_data = [False,False,False] #vername,vercode,downLink
        if typ=="web":
            twt = TwtWeb()
            version,sha = twt.version()
            hash_value = sha
            existsing_flag_file = f'flags_{typ}.json'
            os.rename(existsing_flag_file, old_file_name)
            # os.remove(existsing_flag_file)
            fs = twt.featureSwitches()
            makeJsonFile(existsing_flag_file,fs)
            shutil.copy(existsing_flag_file, new_file_name)
            down_data = [typ,version,False]

        else:
            
            if source == "apt":
                down_data = downTwt2(typ)
            else:
                down_data = downTwt(typ)
            if not down_data[0]: 
                return False
            
            existsing_flag_file = f'flags_{typ}.json'
            shutil.copyfile(existsing_flag_file, old_file_name)

            s = unzipper()
            if not s:
                return False
            os.remove(existsing_flag_file)
            shutil.copy(new_file_name, existsing_flag_file)
        
        d = {'version_name': down_data[0],'vercode': down_data[1],'hash':hash_value,'download_link':down_data[2]}
        makeJsonFile(manifest_file_name,d)

        return True
    except Exception as e:
        print(str(e))

    return False


s = main(typ)
print(s)
