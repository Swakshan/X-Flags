from constants import (
    getChannelLink,
    getAPKMCode,
    getAPKMSlug,
    getPackageName,
    getPinMsgID,
    MANIFEST_FILE_NAME,
)
from enums import *
class DATA:
    def __init__(
        self, vername, link, msg_id, src, platform, typ, app, isPairip=False
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
        elif app == Application.GROK:
            self.emoji = "🤖"
        else:
            print("WTF: app name")
        self.vercode = self.vercodeMaker()
        
    def vercodeMaker(self):
        vername = self.vername
        if self.platform == Platform.ANDROID:
            vercode = (
                vername.replace("-alpha.", "20")
                .replace("-beta.", "10")
                .replace("-release.", "00")
            )
            sps = vercode.split(".")
            midCode = "%02d" % int(sps[1])
            return "3" + sps[0] + midCode + sps[len(sps) - 1]
        elif self.platform == Platform.IOS:
            return "3" + vername.replace(".", "")
        elif self.platform == Platform.WEB:
            return vername
        else:
            raise Exception("Cant make vercode")
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
            json_map["pairip"],
        )
    def toJSON(self):
        rd = {}
        rd["msg_id"] = self.msg_id
        rd["src"] = self.src.value
        rd["vername"] = self.vername
        rd["type"] = self.typ.value
        rd["platform"] = self.platform.value
        rd["app"] = self.app.value
        rd["link"] = self.link
        rd["pairip"] = self.pairip
        return rd
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
        pin_link = f"{getChannelLink()}/{getPinMsgID(self.app)}"
        appName = self.app.value
        platform = self.platform.value
        typ = self.typ.value
        emoji = self.emoji
        link = self.link
        vername = self.vername
        rd = f"{emoji} *{appName.upper()} Update* {emoji}\n"
        rd = f"{rd}\n_Platform:_ *{platform.title()}*"
        if platform == Platform.WEB.value:
            rd = f"{rd}\n_Hash_:\n`{vername.split("||")[0]}`"
            linkRowFormer("Web Link", link)
            linkRow = linkRow[:-3] + "\n"
        else:
            rd = f"{rd}\n_Type:_ *{typ.upper()}*"
            rd = f"{rd}\n_Version:_ `{vername}`"
            if self.app == Application.X:
                rd = f"{rd}\n_Vercode:_ `{self.vercode}`"
            prStr = (
                "🚫App contains PairipLib🚫"
                if self.pairip
                else "❇️App does not contain PairipLib❇️"
            )
            rd = f"{rd}\n\n{prStr}"
        if platform == Platform.ANDROID.value:
            pkgName = getPackageName(self.app)
            apkmCode = getAPKMCode(self.app)
            apkmSlug = getAPKMSlug(self.app)
            
            ps_link = "https://play.google.com/store/apps/details?id=" + pkgName
            apkp_link = f"https://d.apkpure.com/b/XAPK/{pkgName}?versionCode={self.vercode}"
            apkm_vername = vername.replace(".", "-")
            apkm_verSlug = f"{apkmSlug}-{apkm_vername}"
            apkm_link = f"https://www.apkmirror.com/apk/{apkmCode}/{apkm_verSlug}-release/{apkm_verSlug}-android-apk-download/"
            
            if "aptoide" in link:
                linkRowFormer("Aptoide", link)
            linkRowFormer("Play Store", ps_link)
            linkRowFormer("ApkMirror", apkm_link)
            linkRowFormer("APKPure", apkp_link)
        elif platform == Platform.IOS.value:
            linkRowFormer("Apple Store", link)
            linkRow = linkRow[:-3] + "\n"
        linkRow = linkRow + "\n" if linkRow[-2] == "|" else linkRow
        if len(self.changeLogs):
            rd = f"{rd}\n\n__Changelogs:__\n{self.changeLogs}"
        rd = f"{rd}\n\n{linkRow}----------------------------\n[Other {appName.title()} Versions]({pin_link})"
        rd = f"{rd}\n----------------------------\n{flagData}"
        rd = f"{rd}\n\n#{appName.capitalize()} #{typ} #{platform}"
        return rd
    def __repr__(self):
        return str(self.toJSON())