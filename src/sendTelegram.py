from compare import flagMessage
from constants import MANIFEST_FILE_NAME,getEnv,isDebug,getTopicID
from basics import readJson,printSubCmd
from tele import editMsg
from model import DATA

def sendMessage(manifest):
    data:DATA = DATA.fromJSON(manifest)

    flagMsg = flagMessage(data)
    teleMsg = data.teleMsg(flagMsg)
    
    topicId = getTopicID(data.app)
    editMsg(msgId=data.msg_id,text=teleMsg,topic_id=topicId)

if not isDebug():
    manifest = readJson(MANIFEST_FILE_NAME)
    if manifest['sts']:
        if int(getEnv("SHARE_TO_TELE")):
            sendMessage(manifest)
        else:
            printSubCmd("share to tele is false, so skipping reporting telegram","!")
    else:
        printSubCmd("Status is false, so skipping reporting telegram","!")