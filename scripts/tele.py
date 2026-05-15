import requests
from basics import get_exception,printJson,printSubCmd
from common import getEnv
from constants import getChannelId

spl_ch = ['**',  '``', '[[', ']]', '((', '))', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' ]
def santizeText(txt):
  for ch in spl_ch:
    txt = txt.replace(ch,f'\\{ch}')
  return txt

def sendMsg(text,topic_id="0",tag="untitled"):
    printSubCmd("Telegram sending message")
    BOT_TOKEN = getEnv("BOT_TOKEN")
    channel_id = getChannelId()
    tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage'
    text = santizeText(text)
    cont = {
        "chat_id":channel_id,
        "text":text,
        "disable_web_page_preview":1,
        "parse_mode" : "MarkdownV2"
    }
    if int(topic_id):
        cont['message_thread_id'] = topic_id
    try:
        req = requests.post(tele_api_send_msg,data=cont)
        pkjson = req.json()
        if req.status_code==200:
            new_msg_id = pkjson['result']['message_id']
            rd = new_msg_id
            printSubCmd(f"Telegram Uploaded: {tag}")
            # pinMsg(chat_id,new_msg_id,tag)
        else:
            printSubCmd("Telegram action failed","x")
            printJson(pkjson)
            rd = False
        return rd
    except Exception as e:
        print(get_exception())
        return False

def editMsg(msgId,text,topic_id="0"):
    printSubCmd("Telegram editting message")
    BOT_TOKEN = getEnv("BOT_TOKEN")
    channel_id = getChannelId()
    tele_api_edit_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/editMessageText'
    txt = santizeText(text)
    cont = {
        "chat_id":channel_id,
        "message_id":msgId,
        "text":txt,
        "disable_web_page_preview":1,
        "parse_mode" : "MarkdownV2",
    }
    if int(topic_id):
        cont['message_thread_id'] = topic_id
    try:
        req = requests.post(tele_api_edit_msg,data=cont)
    
        pkjson = req.json()
        if req.status_code==200:
            new_msg_id = pkjson['result']['message_id']
            printSubCmd("Telegram message editted")
            return new_msg_id
        else:
            printSubCmd("Telegram action failed","x")
            printJson(pkjson)
            new_msg_id = False
        return new_msg_id
    except Exception as e:
        print(get_exception())
        return False