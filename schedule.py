import sys
import time
import argparse
import datetime
import requests
from booking import *
from structure import AsciiArt
FAULTLIMIT = 64


def timeprint(text):
    print("({:s}) {:s}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), text), flush=True)


parser = argparse.ArgumentParser(description="TKB AutoBooking Script.")
parser.add_argument("--account", "-a", required=True, help="Account(ID Number)")
parser.add_argument("--password", "-p", required=True, help="Password")
parser.add_argument("--txtpath", "-t", required=True, help="Path of task.txt")
parser.add_argument("--nocheck", "-n", required=False, default=False, action='store_true')
args = parser.parse_args()
print(AsciiArt.logo)
fault, delay = 0, 0
noon = True if (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).hour <= 12 else False
targetdate = datetime.datetime.utcnow() + datetime.timedelta(days=6 if noon else 7, hours=8)
targetstr = targetdate.strftime("%Y-%m-%d")
sleepstamp = (targetdate.replace(hour=12 if noon else 0, minute=0, second=0, microsecond=0)
              - datetime.timedelta(days=6)).timestamp()
sleepstr = datetime.datetime.fromtimestamp(sleepstamp).strftime('%Y-%m-%d %H:%M:%S.%f')
file = open(args.txtpath, 'r')
task = dict()
timeprint("目前的模式為：{:s}.".format("午間觸發" if noon else "夜間觸發"))
timeprint("預計的觸發時間為：{:s} UTC+8".format(sleepstr))
timeprint("預計要預約的日期為：{:s}.".format(targetstr))
session = requests.Session()  # create session
session.headers.update({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/67.0.3396.99 Safari/537.36"})
timeprint("成功建立Session，準備登入...")
while fault < FAULTLIMIT:  # login loop
    if login(session, username=args.account, password=args.password):
        timeprint("登入成功.")
        for l in file.read().splitlines():  # read data
            data = l.split('*')
            task[data[0]] = [data[1], data[2], data[3].split(' ')]
        break
    else:
        timeprint("登入失敗, 1秒後重試...")
        time.sleep(1)
        fault += 1
if targetstr in task:
    data = task[targetstr]
    timeprint("已確定預計預約日有排定的預約.")
    timeprint("正在取得訂位頁Access token...")
    gettoken = getbooktoken(session)   # get token
    token = None
    if gettoken[0] == TokenResponse.OK:
        token = gettoken[1]
        timeprint("已成功取得Access token.")
    else:
        timeprint("取得Access token失敗，按Enter結束...")
        input()
        sys.exit(0)
    timeprint("正在計算與Server間的Delay...")
    delay = getserverdelay()
    timeprint("Delay為:{:.5f}s.".format(delay))
    sleepstamp -= delay
    sleepstr = datetime.datetime.fromtimestamp(sleepstamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    timeprint("觸發時間修正為：{:s} UTC+8.".format(sleepstr))
    timeprint("開始等待觸發時間到達...")
    while True:  # sleep until time up
        stampnow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).timestamp()
        if (sleepstamp - stampnow) <= 0:
            break
        else:
            time.sleep(0.1)
    while fault < FAULTLIMIT:  # booking loop
        result = booking(session, data[0], data[1], targetstr, data[2], token=token, nocheck=args.nocheck)
        if result == BookingResponse.OK:
            timeprint("預約成功.")
            print(AsciiArt.success)
            break
        else:
            timeprint(result.value)
            fault += 1
    timeprint("開始取得學堂預約狀況...")
    scheduletime = gettime(session, data[0], targetstr)
    for t in scheduletime:
        t.print()
else:
    timeprint("持續地登入失敗 或 預計預約日未排程 -> {:s}.".format(targetstr))
timeprint("按Enter結束...")
input()
