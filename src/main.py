import requests,json,os,shutil,sys,zipfile
from appData import ApkCombo,webfeatureSwitches
from tqdm import tqdm
from pprint import pprint
from common import DUMMY_FOLDER,MAIN_FOLDER,ZIP_FILE,EXTRACT_FOLDER,PKG_NAME,APP_NAME,new_file_name,old_file_name,DEBUG,manifest_file_name,Platform,Releases,new_file_ipad_name,old_file_ipad_name
from common import writeJson,readJson,get_exception,vercodeGenerator,headers

VER = "v9.3 : minor code refactoring"


vername = "web"
source = "web"
vercode = ""
down_link = ""


def downloader(url,fileName="",isJson=False):
    print(f"Downloading: {fileName}")
    response = requests.get(url, stream=True,headers=headers())
    if not isJson:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(ZIP_FILE, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
    else:
        js = response.json()
        writeJson(fileName,js)
    


def unzipper(platform):
    try:
        def extract(src,new_name):
            try:
                zip_obj.extract(src,path=EXTRACT_FOLDER)
                fg = readJson(EXTRACT_FOLDER +src)
                writeJson(new_name,fg)
                return True
            except Exception as e:
                print(get_exception())
                return False

        feature_file = False
        zip_obj = zipfile.ZipFile(ZIP_FILE, 'r')
        file_list = zip_obj.namelist()
        
        if platform == Platform.ANDROID:
            FLAG_FOLDER ="res/raw"
            FLAG_FILE = f"{FLAG_FOLDER}/feature_switch_manifest" 
            apk_name = f'{PKG_NAME}.apk'
            apk_name_2 = f'base.apk'

            if apk_name in file_list or apk_name_2 in file_list:
                apk_name = apk_name_2 if apk_name_2 in file_list else apk_name
                zip_obj.extract(apk_name, path=EXTRACT_FOLDER)
                zip_obj = zipfile.ZipFile(EXTRACT_FOLDER+apk_name, 'r')
                feature_file = True

            elif FLAG_FILE in file_list:
                feature_file = True

            if feature_file:
                return extract(FLAG_FILE,new_file_name)
        
        elif platform == Platform.IOS:
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
        print(get_exception())

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
                # fileName = f"{vername}.{d['apktype']}"
                downloader(downLink)
                return [vername,vercode,False]# if apkcombo dont save the link
            else:
                prinData = "version not Found"
        else:
            prinData = "type not Found"
        print(prinData)
    except Exception as e:
        print(get_exception())
    return False


def main():
    # global vername,source,vercode,down_link
    if len(sys.argv)>1:
        vername = sys.argv[1]
        source = sys.argv[2]
        vercode = sys.argv[3]
        down_link = sys.argv[4]
    vername = vername.lower()
    source = source.lower()
    vercode = vercodeGenerator(vername) if not(vername) else vercode #generate vercode if 0 is provided
    try:    
        hash_value = False
        typ = Releases.WEB.value if "web" in vername else Releases.BETA.value if "beta" in vername else Releases.ALPHA.value if "alpha" in vername else Releases.STABLE.value
        platform = Platform.WEB if "web" in source else Platform.IOS if "ios" in source else Platform.ANDROID
        down_data = [False,False,False] #vername,vercode,downLink
        sts = False
        
        if platform==Platform.WEB:
            sha,fs_hash = vercode.split(":")
            hash_value = sha
            existsing_flag_file = f'flags_{typ}.json'
            os.rename(existsing_flag_file, old_file_name)

            fs = webfeatureSwitches(fs_hash)
            writeJson(existsing_flag_file,fs)
            shutil.copy(existsing_flag_file, new_file_name)
            down_data = [typ,fs_hash,False]
            sts = True
        
        elif platform==Platform.IOS:
            vercode = ""
            if ".json" in down_link:
                downloader(url=down_link,fileName=new_file_name,isJson=True)
                downloader(url=down_link,fileName=new_file_ipad_name,isJson=True)
            else:
                downloader(down_link)
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
            sts = True
            
        elif platform==Platform.ANDROID:
            if source== "manual" or source == "apt":
                # fileName = f"{vername}.apk"
                downloader(down_link)
                down_link = False if source== "manual" else down_link
                down_data = [vername,vercode,down_link]
            else:
                down_data = downTwt(typ) #apkcombo
                if not down_data[0]: 
                    raise Exception("Error downloading")
            
            existsing_flag_file = f'flags_android_{typ}.json'
            shutil.copyfile(existsing_flag_file, old_file_name)

            s = unzipper(platform)
            if not s:
                raise Exception("Error unzipping")
            os.remove(existsing_flag_file)
            shutil.copy(new_file_name, existsing_flag_file)
            sts = True
            
        d = {'sts':sts,'version_name': down_data[0],'vercode': down_data[1],'hash':hash_value,'download_link':down_data[2],'os':platform.value}

    except Exception as e:
        d = {'sts':sts}
        print(get_exception())

    writeJson(manifest_file_name,d)
    return sts

if not DEBUG:
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    os.makedirs(MAIN_FOLDER)

    s = main()
    print(s)