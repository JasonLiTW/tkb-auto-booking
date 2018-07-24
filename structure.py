from enum import Enum


class BookingClass:
    def __init__(self, bselem):
        self.value = bselem.attrs["value"]
        self.string = bselem.text.replace('\xa0', ' ')

    def print(self):
        print(self.value, self.string)


class BookingDate:
    def __init__(self, data):
        self.value = data["DATE_VALUE"]
        self.string = data["DATE_STRING"].replace('\xa0', ' ')

    def print(self):
        print(self.value, self.string)


class BookingBranch:
    def __init__(self, data):
        self.name = data["BRANCH_NAME"].replace('\xa0', ' ')
        self.expiredate = data["EFFECTIVE_DATE"]
        self.value = data["LOCATION"]

    def print(self):
        print(self.value, self.name, self.expiredate)


class BookingTime:
    def __init__(self, data):
        self.value = data["SEGMENT"]
        self.seatnum = data["ALLSEAT"]
        self.remaining = data["SEATNUM"]
        self.openrate = data["OPEN_RATE"]
        self.starttime = data["INIT_TIME"]
        self.endtime = data["END_TIME"]
        self.stop = True if data["OFFCLASS"] == "1" else False
        self.reserved = True if data["HASCLASS"] == "1" else False

    def print(self):
        print(self.value, self.starttime, "~", self.endtime,
              (str(int(self.seatnum) - int(self.remaining)) + "/" + self.seatnum), ("Close" if self.stop else ""),
              ("Reserved" if self.reserved else ""))


class BookingResponse(Enum):
    OK = "預約成功"
    NOCONTINOUS = "無連續座位"
    FAIL = "預約失敗"
    NOTAVAILABLE = "該時間不可預約"
    TIMEOUT = "Timeout錯誤"


class CheckingResponse(Enum):
    OK = "檢查OK"
    CLASSNOTREACHABLE = "可上課程取得發生錯誤"
    BRANCHNOTREACHABLE = "可上課地點取得發生錯誤"
    DATENOTREACHABLE = "可上課日期取得發生錯誤"
    TIMENOTREACHABLE = "可上課時段取得發生錯誤"


class TokenResponse(Enum):
    OK = "成功獲得Token"
    FAIL = "獲得TOKEN失敗"


class AsciiArt:
    logo = """
    
////////////////////////////////////////////////////////////////////////////
_/_/_/_/_/  _/    _/  _/_/_/                             author: JasonLiTW
   _/      _/  _/    _/    _/                                      2018.07
  _/      _/_/      _/_/_/ 
 _/      _/  _/    _/    _/
_/      _/    _/  _/_/_/   

      _/_/    _/    _/  _/_/_/_/_/    _/_/
   _/    _/  _/    _/      _/      _/    _/
  _/_/_/_/  _/    _/      _/      _/    _/
 _/    _/  _/    _/      _/      _/    _/
_/    _/    _/_/        _/        _/_/

    _/_/_/      _/_/      _/_/    _/    _/  _/_/_/  _/      _/    _/_/_/
   _/    _/  _/    _/  _/    _/  _/  _/      _/    _/_/    _/  _/      
  _/_/_/    _/    _/  _/    _/  _/_/        _/    _/  _/  _/  _/  _/_/ 
 _/    _/  _/    _/  _/    _/  _/  _/      _/    _/    _/_/  _/    _/  
_/_/_/      _/_/      _/_/    _/    _/  _/_/_/  _/      _/    _/_/_/   
////////////////////////////////////////////////////////////////////////////

    """
    success = """
    
    ////////////////////////////////////////////////////////////////////////////
          _/_/_/  _/    _/    _/_/_/    _/_/_/  _/_/_/_/    _/_/_/    _/_/_/  _/
       _/        _/    _/  _/        _/        _/        _/        _/        _/ 
        _/_/    _/    _/  _/        _/        _/_/_/      _/_/      _/_/    _/  
           _/  _/    _/  _/        _/        _/              _/        _/       
    _/_/_/      _/_/      _/_/_/    _/_/_/  _/_/_/_/  _/_/_/    _/_/_/    _/    
    ////////////////////////////////////////////////////////////////////////////
    
    """