import os,json
from sys import exc_info
from traceback import format_exception
from dotenv import load_dotenv

def get_exception():
    etype, value, tb = exc_info()
    info, error = format_exception(etype, value, tb)[-2:]
    return f'Exception in: {info}: {error}'

def printCmd(msg):
    print(f"*************** {msg.upper()} *************")

def printSubCmd(msg,sym="-"):
    print(f"{sym} {msg.capitalize()}")

def printJson(data):
    print(json.dumps(data,indent=4))

def readFile(filename):
    printSubCmd(f"Reading = {filename}")
    f = open(filename,'r',encoding='utf-8')
    d = f.read()
    f.close()
    return d

def writeFile(fileName,data):
    printSubCmd(f"Writing = {fileName}")
    f = open(fileName, 'w')
    f.write(data)
    f.close()

def writeJson(fileName,data):
    printSubCmd(f"Writing = {fileName}")
    f = open(fileName, 'w')
    json.dump(data,f,indent=4)
    f.close()

def readJson(filename):
    printSubCmd(f"Reading = {filename}")
    f = open(filename,'r')
    d = json.load(f)
    f.close()
    return d

def printLine():
    return "*--------------*"