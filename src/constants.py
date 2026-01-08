from dotenv import load_dotenv

from pytz import timezone
import os
from enums import Application
from user_agent import generate_user_agent

load_dotenv()


def getRootDir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

DUMMY_FOLDER = getRootDir() + '/dummy/'
ZIP_FILE = DUMMY_FOLDER + 'app.zip'
EXTRACT_FOLDER = DUMMY_FOLDER + 'Extracted/'
MAIN_FOLDER = DUMMY_FOLDER + 'main/'
OLD_FILE_NAME = MAIN_FOLDER + 'old_feature_data.json'
NEW_FILE_NAME = MAIN_FOLDER + 'new_feature_data.json'
CHANGES_FILE_NAME = MAIN_FOLDER + 'changes.json'
MANIFEST_FILE_NAME = "manifest.json"
NEW_FLAG_LIMIT = 10
USERNAME = "Swakshan"
REPO_NAME = "X-Flags"


def getEnv(data):
    try:
        return os.environ.get(data)
    except Exception as e:
        print(str(e))
        return "0"


def isDebug():
    return int(getEnv("DEBUG"))

def getChannelId():
    return getEnv("CHANNEL_ID")

def getChannelName():
    return getChannelId().replace("-100","") if isDebug() else getEnv("CHANNEL_NAME")

def getTopicID(app: Application):
    debug = isDebug()
    if app == Application.X:
       return getEnv("TOPIC_ID_X")
    if app == Application.GROK:
       return getEnv("TOPIC_ID_GROK")

def getPinMsgID(app: Application):
    if app == Application.X:
        return getEnv("PINNED_MSG_X")

    if app == Application.GROK:
        return getEnv("PINNED_MSG_GROK")


def getPackageName(app: Application):
    if app == Application.X:
        return "com.twitter.android"

    if app == Application.GROK:
        return "ai.x.grok"


def getAPKMCode(app: Application):
    if app == Application.X:
        return "x-corp/twitter"

    if app == Application.GROK:
        return "xai/grok"
    
def getAPKMSlug(app: Application):
    if app == Application.X:
        return "x"

    if app == Application.GROK:
        return "grok-ai-assistant"


def getUptoCode(app: Application):
    if app == Application.X:
        return "16792"

    if app == Application.GROK:
        return "1000312412"


def getAppleStoreCode(app: Application):
    if app == Application.X:
        return "id333903271"

    if app == Application.GROK:
        return "id6670324846"


def headers():
    return {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": generate_user_agent()
    }
