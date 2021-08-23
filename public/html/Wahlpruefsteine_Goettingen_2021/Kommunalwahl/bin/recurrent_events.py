import sys
import os
import json
import re
from datetime import date, datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

recurrInterval = 20 # Interval to compile recurring events


def importISOtime(dateISO):
    """
    imports some ISO formatted time string into datetime format
    """
    conformed_dateISO = re.sub(r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))", '', dateISO)
    return datetime.strptime(conformed_dateISO, "%Y%m%dT%H%M%S%f%z")

def list_of_files_in_base(base):
    """
    leaves out links in order to avoid infinite recursion
    """
    LoF = []
    try:
        for item in os.listdir(base):
            print (item)
            if os.path.isfile(base + "/" + item) and item[-3:] == ".md":
                LoF.append(os.path.join(base,item))
    except OSError:
        None
    return LoF

def nth_weekday(the_date, nth_week, week_day):
    if nth_week > 0:
        # first day in month
        ret = the_date.replace(day=1)
        adj = (week_day - ret.weekday()) % 7
        ret += timedelta(days=adj)
        ret += timedelta(weeks=nth_week-1)
    elif nth_week < 0:
        # last day in month, first in next month minus 1
        ret = date(the_date.year + (the_date.month == 12), 
              (the_date.month + 1 if the_date.month < 12 else 1), 1) - timedelta(1)
        adj = (ret.weekday() - week_day) % 7
        ret -= timedelta(days=adj)
        ret -= timedelta(weeks=-(nth_week+1))
    else:
        ret = the_date
    return ret
    
def getNextDate(xDate, dateInterval):
    if dateInterval[1] == "first":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), 1, xDate.timetuple()[6])
    elif dateInterval[1] == "second":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), 2, xDate.timetuple()[6])
    elif dateInterval[1] == "third":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), 3, xDate.timetuple()[6])
    elif dateInterval[1] == "fourth":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), 4, xDate.timetuple()[6])
    elif dateInterval[1] == "last":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), -1, xDate.timetuple()[6])
    elif dateInterval[1] == "2ndlast":
        ret = nth_weekday(xDate + relativedelta(years=0,months=1,days=0), -2, xDate.timetuple()[6])
    else:
        ret = xDate + relativedelta(years=dateInterval[0],months=dateInterval[1],days=dateInterval[2])
    return ret
        
def compileEvents(recurrEvtFile):
    """
    compiles recurrent events in given timeframe of the front matter json
    """
    
    try:
        evtInFF = open(recurrEvtFile, "r")
        print ("opened file: " + recurrEvtFile)
    except:
        print ("could not open file: " + recurrEvtFile)

    Data = ""
    jsonFound = False
    for line in evtInFF:
        Data += line
        if not jsonFound:
            try:
                evtRecurr = json.loads(Data)
                jsonFound = True
                Data = ""
            except:
                None
    date_now = date.today()
    minDate = date_now
    maxDate = date_now + timedelta(days=int(recurrInterval))
    # print (datetime.now().isoformat())

    try:
        dateStart = evtRecurr["recurring"][0]["start"]
    except:
        dateStart = minDate # defaults to now
    try:
        dateEnd = evtRecurr["recurring"][0]["end"]
    except:
        dateEnd = maxDate  # defaults to the given interval 
    try:
        dateInterval = evtRecurr["recurring"][0]["interval"]
    except:
        dateInterval = [0,0,7] # defaults to weekly event
    try:
        dateIterations = evtRecurr["recurring"][0]["iterations"]
    except:
        dateIterations = -1  # defaults to infinity
    try:
        InitDateTime = importISOtime(dateStart)
        InitWeekday = InitDateTime.timetuple()[6]
        print (InitDateTime.strftime("%A") + ": " + InitWeekday)
    except:
        InitDate = None # no default here
    try:
        Duration = evtRecurr["duration"]
    except:
        Duration = None # no default here
    try:
        Title = evtRecurr["title"]
    except:
        Title = None # no default here
    try:
        Subtitle = evtRecurr["subtitle"]
    except:
        Subtitle = None # no default here
    try:
        Author = evtRecurr["author"]
    except:
        Author = None # no default here
    try:
        Place = evtRecurr["place"]
    except:
        Place = None # no default here
    try:
        Image = evtRecurr["image"]
    except:
        Image = None # no default here
    try:
        Icon = evtRecurr["icon"]
    except:
        Icon = None # no default here
    
    DateTimeStart = datetime.strptime(dateStart, "%Y-%m-%dT%H:%M:00+01:00") 
    DateTimeEnd = datetime.strptime(dateEnd, "%Y-%m-%dT%H:%M:00+01:00") 
    DateStart = DateTimeStart.date()
    DateEnd = DateTimeEnd.date()

    
    print (json.dumps(evtRecurr))
    # print (Data)
    # print (dateStart, dateInterval, minDate, maxDate, minDate > maxDate )


    
    iter = 0
    xDate = DateStart
    while xDate <=  maxDate and xDate <= DateEnd and (iter < dateIterations or dateIterations < 0 ):
        if xDate >= minDate:
            print ('->', xDate)
            xdate = xDate.strftime("%Y-%m-%d")
            xtime = InitDateTime.strftime("%H:%M")

            xDate.strftime("/%Y/%m/%d/")
            InitDateTime.strftime("%H/%M/")
            

            try:
                url_title = ""
                k = 0
                for word in Title.split():
                    url_title += "-" + word.replace("/","-").lower()
                    if k > 3:
                        break
                evtOutFN = targetDir + str(xDate) + url_title + ".md"
                evtOutFF = open(evtOutFN, "w")
                evtOutFF.write("---\n")
                evtOutFF.write("layout:        \"events\"\n")
                evtOutFF.write("title:         \"" + Title + "\"\n")
                evtOutFF.write("subtitle:      \"" + Subtitle + "\"\n")
                evtOutFF.write("date:          " + xdate + "T" + xtime + ":00+01:00\n")
                evtOutFF.write("publishdate:   " + date_now.strftime("%Y-%m-%dT%H:%M:00+01:00") + "\n")
                evtOutFF.write("author:        \"" + Author  + "\"\n")
                evtOutFF.write("place:         \"" + Place + "\"\n")
                evtOutFF.write("image:         \"" + Image + "\"\n")
                evtOutFF.write("icon:         \"" + Icon + "\"\n")
                evtOutFF.write("URL:           \"" + xDate.strftime("/%Y/%m/%d/") + InitDateTime.strftime("%H/%M") + url_title + "\"\n")
                evtOutFF.write("---\n\n\n")
                evtOutFF.write(Data)
                evtOutFF.close()
            except:
                print ("could not open file: " + evtOutFN)
        else:
            print ('--', xDate)
        xDate = getNextDate(xDate, dateInterval)
    evtInFF.close()


#### main ####
if __name__ == '__main__':
    baseDir = "/home/uschwar1/ownCloud/AC/html/hugo/goest/content/event/"
    if (len(sys.argv) == 2):
        baseDir = sys.argv[1]
        if baseDir[-1] != "/":
            baseDir += "/"
    sourceDir = baseDir + "recurring_templates/"
    targetDir = baseDir + "recurring/"

    LoF = list_of_files_in_base(sourceDir)
    print (sourceDir)
    print (LoF)
    
    for file in LoF:
        # print (file)
        compileEvents(file)





    sys.exit(0)
    # a = datetime.now(timezone.utc)
    # c = a - dateTime
    # # timedelta(0, 8, 562000)
    # # delta = divmod(c.days * 86400 + c.seconds, 60)
    # print (c.days, date1)
    
