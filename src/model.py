from dataclasses import dataclass
from enum import Enum


@dataclass
class DownloadData:
    vername: str
    vercode: str
    downLink: str
    hash: str #used in web

class Platform(Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

class Releases(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"
    WEB = "web"

class Source(Enum):
    MAN = "manual"
    WEB = Releases.WEB.value
    IOS = "stable_ios"
    APT = "aptoide"
    APKC = "apkcombo"
    APKM = "apkmirror"
    DK= "dontknow"

    @classmethod
    def _missing_(Source, value):
        return Source.DK
