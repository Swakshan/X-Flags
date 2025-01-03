import requests
from common import get_exception,getEnv,printJson


spl_ch = ['**',  '``', '[[', ']]', '((', '))', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!' ]
def santizeText(txt):
  for ch in spl_ch:
    txt = txt.replace(ch,f'\\{ch}')
  return txt

def sendMsg(chat_id,text="",tag="untitled"):
    BOT_TOKEN = getEnv("BOT_TOKEN")
    tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage'
    text = santizeText(text)
    cont = {
        "chat_id":chat_id,
        "text":text,
        "disable_web_page_preview":1,
        "parse_mode" : "MarkdownV2"
    }
    try:
        req = requests.post(tele_api_send_msg,data=cont)
        pkjson = req.json()
        if req.status_code==200:
            printData = (f'Uploaded: {tag}')
            new_msg_id = pkjson['result']['message_id']
            rd = new_msg_id
            # pinMsg(chat_id,new_msg_id,tag)
        else:
            printJson(pkjson)
            printData ="Upload Error"
            rd = False
        print(printData)
        return rd
    except Exception as e:
        print(get_exception())
        return False

def editMsg(chat_id,msgId,txt="Edited"):
    BOT_TOKEN = getEnv("BOT_TOKEN")
    tele_api_edit_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/editMessageText'
    txt = santizeText(txt)
    cont = {
        "chat_id":chat_id,
        "message_id":msgId,
        "text":txt,
        "disable_web_page_preview":1,
        "parse_mode" : "MarkdownV2",
    }
    req = requests.post(tele_api_edit_msg,data=cont)
    try:
        pkjson = req.json()
        if req.status_code==200:
            new_msg_id = pkjson['result']['message_id']
            return new_msg_id
        else:
            print("Cant Edit in Tele")
            print(pkjson)
            new_msg_id = False
        return new_msg_id
    except Exception as e:
        print(get_exception())
        return False