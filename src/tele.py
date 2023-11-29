import requests,json
import os,sys
from common import BOT_TOKEN,get_exception


def printJson(data):
    print(json.dumps(data,indent=4))

tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage?chat_id={chat_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'
tele_api_edit_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/editMessageText?chat_id={chat_id}&message_id={message_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'

def sendMsg(chat_id,text="",tag="untitled"):
    text = text.replace('.','\\.').replace('-','\\-').replace('|','\\|')
    api = tele_api_send_msg.format(chat_id=chat_id,text = text)
    try:
        req = requests.post(api)
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
    txt = txt.replace('.','\\.').replace('-','\\-').replace('|','\\|')
    api = tele_api_edit_msg.format(chat_id=chat_id,message_id=msgId,text=txt)
    req = requests.post(api)
    try:
        pkjson = req.json()
        if req.status_code==200:
            new_msg_id = pkjson['result']['message_id']
            # pinMsg(chat_id,new_msg_id)
            return new_msg_id
        else:
            print("Cant Edit in Tele")
            print(pkjson)
            new_msg_id = False
        return new_msg_id
    except Exception as e:
        print(get_exception())
        return False