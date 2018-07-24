import json
import datetime
import requests
from structure import *
from bs4 import BeautifulSoup
from time import mktime, strptime
FAULTLIMIT = 64


def login(sess, username="", password=""):
    try:
        html = sess.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index").text
        bsobj = BeautifulSoup(html, "lxml")
        token = bsobj.find("input", {"name": "access_token"}).attrs["value"]
        payload = {"access_token": token, "toURL": "/student/bookSeat/index", "id": username, "pwd": password}
        status = sess.post("http://bookseat.tkblearning.com.tw/book-seat/student/login/login", allow_redirects=False,
                           data=payload).status_code
        if status == 302:
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        return False


def getbooktoken(sess):
    fault = 0
    while fault < FAULTLIMIT:
        try:
            html = sess.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index").text
            token = html.split('access_token : \"')[1].split('\"')[0]
            return TokenResponse.OK, token
        except:
            fault += 1
            continue
    return TokenResponse.FAIL, None


def getclass(sess):
    try:
        html = sess.get("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index").text
        bsobj = BeautifulSoup(html, "lxml")
        selector = bsobj.find("select", {"id": "class_selector"}).findAll("option")
        data = [BookingClass(cls) for cls in selector if len(cls.attrs["value"]) > 0]
        return data
    except:
        return []


def getdate(sess, classid, expiredate):
    try:
        payload = {"effectiveDate": expiredate, "class_data": classid, "class_status": "T"}
        html = sess.post("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/canBookseatDate",
                         data=payload).text
        jsondata = json.loads(html)
        data = [BookingDate(d) for d in jsondata]
        return data
    except:
        return []


def getbranch(sess, classid):
    try:
        payload = {"class_data": classid}
        html = sess.post("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/branch", data=payload).text
        jsondata = json.loads(html)
        data = [BookingBranch(b) for b in jsondata]
        return data
    except:
        return []


def gettime(sess, branchid, date):
    try:
        payload = {"date": date, "branch_no": branchid}
        html = sess.post("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/sessionTime", data=payload).text
        jsondata = json.loads(html)
        data = [BookingTime(t) for t in jsondata]
        return data
    except:
        return []


def checkavailable(sess, branchid, classid, date, timearr):
    checkclass, checkdate, checktime = False, False, True
    checkbranch, expire = False, ""

    for c in getclass(sess):
        if c.value == classid:
            checkclass = True
    if not checkclass:
        return CheckingResponse.CLASSNOTREACHABLE

    for b in getbranch(sess, classid):
        if b.value == branchid:
            checkbranch = True
            expire = b.expiredate
    if not checkbranch:
        return CheckingResponse.BRANCHNOTREACHABLE

    for d in getdate(sess, classid, expire):
        if d.value == date:
            checkdate = True
    if not checkdate:
        return CheckingResponse.DATENOTREACHABLE

    time = gettime(sess, branchid, date)
    timeok = set([t.value for t in time if t.reserved == "0" and t.remaining != "0"])
    for t in timearr:
        if t not in timeok:
            checktime = False
    if not checktime:
        return CheckingResponse.TIMENOTREACHABLE
    return CheckingResponse.OK


def booking(sess, branchid, classid, date, timearr, token="", nocheck=False):
    if not (nocheck or checkavailable(sess, branchid, classid, date, timearr)):
        return BookingResponse.NOTAVAILABLE
    if token == "":  # no token provided in advance
        result = getbooktoken(sess)
        if result[0] == TokenResponse.OK:
            token = result[1]
        else:
            return BookingResponse.FAIL
    payload = [("access_token", token), ("class_data", classid), ("date", date), ("branch_no", branchid)]
    for time in timearr:
        payload.append(("session_time[]", str(time)))
    try:
        html = sess.post("http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/book", timeout=180,
                         data=tuple(payload))
    except requests.exceptions.Timeout:
        return BookingResponse.TIMEOUT
    if html.status_code == 200:
        jsondata = json.loads(html.text)
        if jsondata["STATUS"] == "1" and jsondata["MESSAGE"] == "預約成功":
            return BookingResponse.OK
        elif jsondata["STATUS"] == "1" and jsondata["BOOKSEAT_STATUS"] == "C":
            return BookingResponse.NOCONTINOUS
    else:
        return BookingResponse.FAIL


def getserverdelay():
    try:
        nowstamp = datetime.datetime.utcnow().timestamp()
        serverdate = requests.get('http://bookseat.tkblearning.com.tw/book-seat/student/bookSeat/index').headers['Date']
        serverstamp = mktime(strptime(serverdate, "%a, %d %b %Y %H:%M:%S %Z"))
        return serverstamp-nowstamp
    except:
        return 0
