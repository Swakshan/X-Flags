from compare import flagMessage
from constants import MANIFEST_FILE_NAME,getEnv,isDebug
from basics import readJson,printSubCmd
from tele import editMsg,sendMsg
from model import DATA

def sendMessage(manifest):
    data:DATA = DATA.fromJSON(manifest)
    
    flagMsg = flagMessage(data)
    teleMsg = data.teleMsg(flagMsg)
    editMsg(data.msg_id,teleMsg)

if not isDebug():
    manifest = readJson(MANIFEST_FILE_NAME)
    if manifest['sts']:
        if int(getEnv("SHARE_TO_TELE")):
            sendMessage(manifest)
        else:
            printSubCmd("share to tele is false, so skipping reporting telegram","!")
    else:
        printSubCmd("Status is false, so skipping reporting telegram","!")