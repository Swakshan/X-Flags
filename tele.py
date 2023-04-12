import requests,json
import os,sys
# from dotenv import load_dotenv
# load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
def printJson(data):
    print(json.dumps(data,indent=4))



tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage?chat_id={chat_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'
tele_api_edit_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/editMessageText?chat_id={chat_id}&message_id={message_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'
# tele_api_send_doc = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendDocument?'
# tele_api_send_doc = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendDocument?chat_id={chat_id}&caption={text}&parse_mode=MarkdownV2'
tele_api_pin_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/pinChatMessage?chat_id={chat_id}&message_id={message_id}'
tele_api_channel = 'https://api.telegram.org/bot'+BOT_TOKEN+'/getChat?chat_id={chat_id}'



def sendMsg(chat_id,text="",tag="untitled"):
    # tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage?chat_id={chat_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'
    
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
        print(str(e))
        return False

def editMsg(chat_id,msgId,txt="Edited"):
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
        print(str(e))
        return False
    
# def pinMsg(chat_id,message_id="",tag="untitled"):
#     # tele_api_send_msg = 'https://api.telegram.org/bot'+BOT_TOKEN+'/sendMessage?chat_id={chat_id}&text={text}&disable_web_page_preview=1&parse_mode=MarkdownV2'
    
#     api = tele_api_pin_msg.format(chat_id=chat_id,message_id=message_id)
#     try:
#         req = requests.post(api)
#         pkjson = req.json()
#         if req.status_code==200:
#             printData = (f'Pinned: {tag}')
#             rd = True
#         else:
#             printJson(pkjson)
#             printData ="Upload Error"
#             rd = 2
#         print(printData)
#         return rd
#     except Exception as e:
#         print(str(e))
#         return False

# def getPinnedMsg(chat_id):
#     api = tele_api_channel.format(chat_id=chat_id)
#     try:
#         req = requests.get(api)
#         pkjson = req.json()
#         if req.status_code==200:
            
#             pnmsg = pkjson['result']['pinned_message']
#             pin_msg_id = pnmsg['message_id']
#             pin_msg = pnmsg['text']
#             ent = pnmsg['entities']
#             pin_msg = entParser(pin_msg,ent)
#             rd=[pin_msg_id,pin_msg]
#         else:
#             printJson(pkjson)
#             printData ="Upload Error"
#             rd = [False,2]
#             print(printData)
#         return rd
#     except Exception as e:
#         print(str(e))
#     return False,False
