import os
from common import readJson
from common import manifest_file_name

def run(cmd):
    os.system(cmd)

sts = readJson(manifest_file_name)
s = sts['sts']
if s:
    commitMsg = sts['commit_msg']

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