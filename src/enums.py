from dataclasses import dataclass
from enum import Enum

class Application(Enum):
    X = "x"
    GROK = "grok"

class Platform(Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

class ReleaseType(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    STABLE = "stable"
    WEB = "web"

class Source(Enum):
    MAN = "manual"
    WEB = "web"
    IOS = "stable_ios"
    APT = "aptoide"
    APKC = "apkcombo"
    APKM = "apkmirror"
    APKP = "apkpure"
    UPTO = "uptodown"
    DK= "DontKnow"

    @classmethod
    def _missing_(Source, value):
        return Source.DK