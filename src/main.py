import requests,json,os,shutil,sys,zipfile
from appData import apkCombo,apkM,webfeatureSwitches
from tqdm import tqdm
from pprint import pprint
from common import DUMMY_FOLDER,MAIN_FOLDER,ZIP_FILE,EXTRACT_FOLDER,PKG_NAME,APP_NAME,new_file_name,old_file_name,DEBUG,manifest_file_name,new_file_ipad_name,old_file_ipad_name
from common import writeJson,readJson,get_exception,vercodeGenerator,headers
from model import DownloadData,Source,Platform,Releases

VER = "v11.2 : updated apkcombo extractor"


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

def downloadAndroid(downData:DownloadData,source:Source):
    url = downData.downLink
    down_link = None
    if source == Source.APKM:
        down_link = apkM(url)
    elif source == Source.APKC:
        down_link = apkCombo(url)
    elif source == Source.MAN or source == Source.APT:
        down_link = url
    else:
        raise Exception("Error: Source "+ source.value +" not found")
    
    if down_link==None:
        raise Exception("Download link not found")
    print(down_link)
    downloader(down_link)

def process(vername,source,vercode,down_link):
    try:        
        typ = Releases.WEB.value if "web" in vername else Releases.BETA.value if "beta" in vername else Releases.ALPHA.value if "alpha" in vername else Releases.STABLE.value
        platform = Platform.WEB if "web" in source else Platform.IOS if "ios" in source else Platform.ANDROID
        source = Source(source)

        # down_data = [False,False,False] #vername,vercode,downLink
        down_data:DownloadData = DownloadData(vername,vercode,down_link,"")
        sts = False
        
        if platform==Platform.WEB:
            sha,fs_hash = vercode.split(":")
            existsing_flag_file = f'flags_{typ}.json'
            os.rename(existsing_flag_file, old_file_name)

            fs = webfeatureSwitches(fs_hash)
            writeJson(existsing_flag_file,fs)
            shutil.copy(existsing_flag_file, new_file_name)
            # down_data = [typ,fs_hash,False]
            down_data.vername = typ
            down_data.vercode = fs_hash
            down_data.downLink = ""
            down_data.hash = sha
            sts = True
        
        elif platform==Platform.IOS:
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

            # down_data = [vername,"",down_link]
            sts = True
            
        elif platform==Platform.ANDROID:
            vercode = vercodeGenerator(vername)
            down_data.vercode = vercode            
            downloadAndroid(down_data,source)
            
            existsing_flag_file = f'flags_android_{typ}.json'
            shutil.copyfile(existsing_flag_file, old_file_name)

            s = unzipper(platform)
            if not s:
                raise Exception("Error unzipping")
            os.remove(existsing_flag_file)
            shutil.copy(new_file_name, existsing_flag_file)
            sts = True
            
        d = {'sts':sts,'version_name': down_data.vername,'vercode': down_data.vercode,'hash':down_data.hash,'download_link':down_data.downLink,'os':platform.value,'src':source.value}

    except Exception as e:
        d = {'sts':sts}
        print(get_exception())

    writeJson(manifest_file_name,d)
    return sts

def main():
    if len(sys.argv)<1:
        raise Exception("Insufficent inputs")
    
    vername = sys.argv[1].lower()
    source = sys.argv[2].lower()
    vercode = sys.argv[3]
    down_link = sys.argv[4]
    
    return process(vername,source,vercode,down_link)


if not DEBUG:
    if os.path.exists(DUMMY_FOLDER):
        shutil.rmtree(DUMMY_FOLDER)
    os.makedirs(MAIN_FOLDER)
    s = main()
    print(s)
