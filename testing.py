from booking import *
from structure import AsciiArt
import requests

print(AsciiArt.logo)
print("輸入帳號:", end='')
acc = input()
print("輸入密碼:", end='')
pwd = input()
session = requests.Session()
session.headers.update({'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like\
 Gecko) Version/10.1 Safari/603.1.30"})
if login(session, username=acc, password=pwd):

    _class = getclass(session)  # 可預約課程
    branch = getbranch(session, _class[0].value)  # 可上課地點: 第一個課程為例
    print("\n可預約課程:")
    for cls in _class:
        cls.print()
    print("\n可上課地點:")
    for brh in branch:
        brh.print()
else:
    print("登入失敗!")