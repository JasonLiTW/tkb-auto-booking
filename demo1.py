from booking import *
import requests

acc = "帳號"
pwd = "密碼"
session = requests.Session()
session.headers.update({'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"})
if login(session, username=acc, password=pwd):
    _class = getclass(session) # 可預約課程
    branch = getbranch(session, _class[0].value) # 可上課地點: 第一個課程為例
    date = getdate(session, _class[0].value, branch[0].expiredate) # 可預約日期
    time = gettime(session, "WB", date[1].value) # 可預約時段: 斗六學堂，日期D+1為例
    print("可預約課程:")
    for cls in _class:
        cls.printOut()
    print("可上課地點:")
    for brh in branch:
        brh.printOut()
    print("可預約日期:")
    for dat in date:
        dat.printOut()
    print("可預約時段:")
    for time in time:
        time.printOut()
    print("檢查可否預約:")
    print(checkavailable(session,"WB" ,_class[2].value ,date[-1].value, ["1", "5"]).value)
    # booking(session, "WB" , classdata[2].value ,datedata[-1].value, ["2", "3", "4"])
