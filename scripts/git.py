import os
from basics import readJson
from constants import MANIFEST_FILE_NAME
from enums import Platform
from model import DATA

def run(cmd):
    os.system(cmd)

manifest = readJson(MANIFEST_FILE_NAME)
s = manifest['sts']
if s:
    data:DATA = DATA.fromJSON(manifest)
    vername = data.vername
    vername = "web: "+vername[:5] if data.platform == Platform.WEB else vername
    commitMsg = f"🤖: {vername}"

    MAIL_ID = "41898282+github-actions[bot]@users.noreply.github.com"
    NAME = "github-actions[bot]"
    run(f'git config --global user.email "{MAIL_ID}"')
    run(f'git config --global user.name "{NAME}"')
    run(f'git pull')
    run(f'git add .')
    run(f'git commit -m "{commitMsg}"')
    run(f'git push')
else:
    print(f'Status : {s}')