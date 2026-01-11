from constants import (
    getChannelName,
    getAPKMCode,
    getAPKMSlug,
    getPackageName,
    getPinMsgID,
    getTopicID,
    MANIFEST_FILE_NAME,
)
from enums import *
class DATA:
    def __init__(
        self, vername, link, msg_id, src, platform, typ, app, vercode,isPairip=False,
    ) -> None:
        self.vername = vername
        self.link = link
        self.msg_id = int(msg_id)
        self.src = src
        self.platform = platform
        self.pairip = False
        self.typ = typ
        self.app = app
        self.pairip = isPairip
        self.emoji = "⚠️"
        self.changeLogs = ""  # grok and IOS has
        
        if app == Application.X:
            self.emoji = "𝕏"
        elif app == Application.XLITE:
            self.emoji = "🚀"
        elif app == Application.GROK:
            self.emoji = "🤖"
        else:
            print("WTF: app name")
        self.vercode = vercode
        
    @classmethod
    def fromJSON(self, json_map: dict):
        src = Source(json_map["src"])
        app = Application(json_map["app"])
        typ = ReleaseType(json_map["type"])
        plt = Platform(json_map["platform"])
        return self(
            json_map["vername"],
            json_map["link"],
            json_map["msg_id"],
            src,
            plt,
            typ,
            app,
            json_map["vercode"],
            json_map["pairip"],
        )
    def toJSON(self):
        rd = {}
        rd["msg_id"] = self.msg_id
        rd["src"] = self.src.value
        rd["vername"] = self.vername
        rd["vercode"] = self.vercode
        rd["type"] = self.typ.value
        rd["platform"] = self.platform.value
        rd["app"] = self.app.value
        rd["link"] = self.link
        rd["pairip"] = self.pairip
        return rd
    
    def __msgLinkGenerator(self,msgId):
        chn_name = getChannelName()
        tele_link = f"https://t.me/{chn_name}"
        topic_id = getTopicID(self.app)
        if int(topic_id):
            return f"{tele_link}/{topic_id}/{msgId}"
        return f"{tele_link}/{msgId}"
    
    def teleMsg(self,flagData):
        global linkRow, linkCount
        linkRow = ""
        linkCount = 0
        def linkRowFormer(name, link):
            global linkRow, linkCount
            tempLink = f"[{name}]({link})"
            linkRow += tempLink
            if linkCount % 2 == 0:
                linkRow += " | "
            else:
                linkRow += "\n"
            linkCount += 1
        
        pin_link = ""
        pinMsgId = getPinMsgID(self.app)
        #XLite doesnt have pin msg
        if pinMsgId:
            pin_link = self.__msgLinkGenerator(pinMsgId)
        appName = self.app.value
        platform = self.platform.value
        typ = self.typ.value
        emoji = self.emoji
        link = self.link
        vername = self.vername
        
        appNameSlug = appName.replace("lite","-lite")
        rd = f"{emoji} *{appNameSlug.upper()} Update* {emoji}\n"
        platformText = platform.title()
        if platform == Platform.IOS.value:
            platformText = "iOS"
        rd = f"{rd}\n_Platform:_ *{platformText}*"
        if platform == Platform.WEB.value:
            rd = f"{rd}\n_Hash_:\n`{vername.split("::")[0]}`"
            linkRowFormer("Web Link", link)
            linkRow = linkRow[:-3] + "\n"
        else:
            rd = f"{rd}\n_Type:_ *{typ.upper()}*"
            rd = f"{rd}\n_Version:_ `{vername}`"
            rd = f"{rd}\n_Vercode:_ `{self.vercode}`"
            
        if platform == Platform.ANDROID.value:
            if self.app in [Application.X,Application.XLITE]:
                prStr = (
                    "🚫App contains PairipLib🚫"
                    if self.pairip
                    else "❇️App does not contain PairipLib❇️"
                )
                rd = f"{rd}\n\n{prStr}"
                
            pkgName = getPackageName(self.app)
            apkmCode = getAPKMCode(self.app)
            apkmSlug = getAPKMSlug(self.app)
            
            ps_link = "https://play.google.com/store/apps/details?id=" + pkgName
            apkp_link = f"https://d.apkpure.com/b/XAPK/{pkgName}?versionCode={self.vercode}"
            apkm_vername = vername.replace(".", "-")
            apkm_verSlug = f"{apkmSlug}-{apkm_vername}"
            apkm_link = f"https://www.apkmirror.com/apk/{apkmCode}/{apkm_verSlug}-release/{apkm_verSlug}-android-apk-download/"
            upto_link = f"https://{appNameSlug}.en.uptodown.com/android"
            
            if "aptoide" in link:
                linkRowFormer("Aptoide", link)
            linkRowFormer("Play Store", ps_link)
            linkRowFormer("ApkMirror", apkm_link)
            linkRowFormer("APKPure", apkp_link)
            linkRowFormer("Uptodown", upto_link)
            
        elif platform == Platform.IOS.value:
            linkRowFormer("Apple Store", link)
            linkRow = linkRow[:-3] + "\n"
        linkRow = linkRow + "\n" if linkRow[-2] == "|" else linkRow
        if len(self.changeLogs):
            rd = f"{rd}\n\n__Changelogs:__\n{self.changeLogs}"
        rd = f"{rd}\n\n{linkRow}----------------------------"
        if len(pin_link): #XLite doesnt have pin msg
            rd = f"{rd}\n[Other {appName.title()} Versions]({pin_link})\n----------------------------"
        rd = f"{rd}\n{flagData}"
        rd = f"{rd}\n\n#{appName.capitalize()} #{typ} #{platform}"
        return rd
    def __repr__(self):
        return str(self.toJSON())