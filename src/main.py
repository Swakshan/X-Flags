import requests,json,os,shutil,sys,zipfile
from appData import ApkCombo, Aptiode,TwtWeb
from tqdm import tqdm
from pprint import pprint
from comman import DUMMY_FOLDER,MAIN_FOLDER,ZIP_FILE,EXTRACT_FOLDER,PKG_NAME,APP_NAME,new_file_name,old_file_name,DEBUG,manifest_file_name,Platform,Releases,new_file_ipad_name,old_file_ipad_name
from comman import writeJson

VER = "v7 : Code refactor & Added iOS support"


vername = "web"
source = "web"
vercode = ""
down_link = ""

vername = vername.lower()
source = source.lower()
vercode = vercode.lower()

if not DEBUG:
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    os.makedirs(MAIN_FOLDER)



def downloader(url,fileName=""):
    print(f"Downloading: {fileName}")
    response = requests.get(url, stream=True)

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(ZIP_FILE, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()


def unzipper(platform):
    try:
        def extract(src,new_name):
            try:
                zip_obj.extract(src,path=EXTRACT_FOLDER)
                os.rename(EXTRACT_FOLDER +src, new_name)
                return True
            except Exception as e:
                print(str(e))
                return False

        feature_file = False
        zip_obj = zipfile.ZipFile(ZIP_FILE, 'r')
        file_list = zip_obj.namelist()
        
        if platform == Platform.ANDROID.value:
            FLAG_FOLDER ="res/raw"
            FLAG_FILE = f"{FLAG_FOLDER}/feature_switch_manifest" 
            apk_name = f'{PKG_NAME}.apk'

            if apk_name in file_list:
                zip_obj.extract(apk_name, path=EXTRACT_FOLDER)
                zip_obj = zipfile.ZipFile(
                    EXTRACT_FOLDER+apk_name, 'r')
                feature_file = True

            elif FLAG_FILE in file_list:
                feature_file = True

            if feature_file:
                return extract(FLAG_FILE,new_file_name)
        
        elif platform == Platform.IOS.value:
            rd1 = False;rd2 = False
            FLAG_FOLDER = "Payload/Twitter.app"
            FLAG_FILE = f"{FLAG_FOLDER}/fs_embedded_defaults_ipad_production.json" 
            if FLAG_FILE in file_list:
                rd1 = extract(FLAG_FILE,new_file_ipad_name)
            
            FLAG_FILE = f"{FLAG_FOLDER}/fs_embedded_defaults_production.json" 
            if FLAG_FILE in file_list:
                rd2 = extract(FLAG_FILE,new_file_name)
            
            return rd1 and rd2
        return False
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
                downloader(downLink,fileName)
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
            downloader(downLink,fileName)
            return [vername,vercode,downLink]
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(str(e))
    return False


def main():
    # global vername,source,vercode,down_link
    if len(sys.argv)>1:
        vername = sys.argv[1]
        source = sys.argv[2]
        vercode = sys.argv[3]
        down_link = sys.argv[4]
    try:    
        hash_value = False
        typ = Releases.WEB.value if "web" in vername else Releases.BETA.value if "beta" in vername else Releases.ALPHA.value if "alpha" in vername else Releases.STABLE.value
        platform = Platform.WEB.value if "web" in source else Platform.IOS.value if "ios" in source else Platform.ANDROID.value
        down_data = [False,False,False] #vername,vercode,downLink
        
        if platform==Platform.WEB.value:
            twt = TwtWeb()
            sha,version = twt.version()
            hash_value = sha
            existsing_flag_file = f'flags_{typ}.json'
            os.rename(existsing_flag_file, old_file_name)
            # os.remove(existsing_flag_file)
            fs = twt.featureSwitches()

            writeJson(existsing_flag_file,fs)
            shutil.copy(existsing_flag_file, new_file_name)
            down_data = [typ,version,False]
        
        elif platform==Platform.IOS.value:
            fileName = "x.ipa"
            vercode = ""
            downloader(down_link,fileName)
            s = unzipper(platform)
            if not s:
                return False
            
            existsing_flag_file = f'flags_iphone_{typ}.json'
            os.rename(existsing_flag_file, old_file_name)
            # os.remove(existsing_flag_file)
            shutil.copy(new_file_name, existsing_flag_file)

            existsing_flag_file = f'flags_ipad_{typ}.json'
            os.rename(existsing_flag_file, old_file_ipad_name)
            # os.remove(existsing_flag_file)
            shutil.copy(new_file_ipad_name, existsing_flag_file)

            down_data = [vername,vercode,down_link]
            
        elif platform==Platform.ANDROID.value:
            if source=="manual":
                fileName = f"{vername}.apk"
                downloader(down_link,fileName)
                down_data = [vername,vercode,False]
            else:
                if source == "apt":
                    down_data = downTwt2(typ)
                else:
                    down_data = downTwt(typ)
                if not down_data[0]: 
                    return False
            
            existsing_flag_file = f'flags_android_{typ}.json'
            shutil.copyfile(existsing_flag_file, old_file_name)

            s = unzipper(platform)
            if not s:
                return False
            os.remove(existsing_flag_file)
            shutil.copy(new_file_name, existsing_flag_file)
            
        d = {'version_name': down_data[0],'vercode': down_data[1],'hash':hash_value,'download_link':down_data[2],'os':platform}
        writeJson(manifest_file_name,d)

        return True
    except Exception as e:
        print(str(e))

    return False


s = main()
print(s)