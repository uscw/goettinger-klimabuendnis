#!/usr/bin/python3
import os
import sys
import uuid
from datetime import date, datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta

homeDir = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis"
outDir = homeDir + "/content/event"
icsDir = homeDir + "/static/ics"
banner_dir = "/img/banner"
def sysCommand(cmd):
   """                                                                                                                          
   executes a system command and prints out: return code, stdout and stderr                                                     
   @param cmd type string: command to execute
   @return out, err type string: output and errors from command
   """
   from subprocess import Popen, PIPE
   # cmd = "ls -l ~/"                                                                                                           
   p = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
   out, err = p.communicate()
   if p.returncode:
      print ("Return code: ", p.returncode)
   return out, err

#####################################

class recurringDates():

    def __init__(self, xDate, DateInterval):
        """
        gives the next date with dateInterval after given date
        self.dateInterval is given as string representing either:
          list of numbers [y,m,d]
             years  = dateInterval[0]
             months = dateInterval[1]
             days   = dateInterval[2]
        or:
          a number of days
  
        @param xDate type string: given date as YYYY-MM-DD
        @param dateInterval type string: interval to next date either  
        """
        self.xDate = datetime.strptime(xDate, "%Y-%m-%d")
        if isinstance(DateInterval, str):
            interval = eval(DateInterval)
        if isinstance(interval, list):
            self.dateInterval = interval
        elif isinstance(interval, int):
            self.dateInterval = [0,0,interval]
        else:
            self.dateInterval = [0,0,0] # repeat the given date
        self.nextDate = self.getNextDate()
        None

    def getNextDate(self):
        if self.dateInterval[1] == "first":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), 1, self.xDate.timetuple()[6])
        elif self.dateInterval[1] == "second":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), 2, self.xDate.timetuple()[6])
        elif self.dateInterval[1] == "third":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), 3, self.xDate.timetuple()[6])
        elif self.dateInterval[1] == "fourth":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), 4, self.xDate.timetuple()[6])
        elif self.dateInterval[1] == "last":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), -1, self.xDate.timetuple()[6])
        elif self.dateInterval[1] == "2ndlast":
            ret = nth_weekday(self.xDate + relativedelta(years=0,months=1,days=0), -2, self.xDate.timetuple()[6])
        else:
            ret = self.xDate + relativedelta(years=self.dateInterval[0],months=self.dateInterval[1],days=self.dateInterval[2])
        return ret

#####################################

class vcal():
   
   def __init__(self,description="",summary="",location="",dtstart="",dtend="",url="",contact=""):
      xmpl = """
BEGIN:VEVENT
DTSTAMP:20250109T081002Z
CREATED:20250109T081002Z
LAST-MODIFIED:20250109T081002Z
SUMMARY:Test Veranstaltung
LOCATION:Test Ort
STATUS:CONFIRMED
PRIORITY:5
RECURRENCE-ID;TZID=W. Europe Standard Time:20160208T000000
DTSTART;TZID=W. Europe Standard Time:20250208T140000
DTEND;TZID=W. Europe Standard Time:20250208T150000
TRANSP:OPAQUE
END:VEVENT
"""
      vevent = """
BEGIN:VEVENT
STATUS:CONFIRMED
TRANSP:OPAQUE
PRIORITY:5
CLASS:PUBLIC
DTSTAMP:00010101T000000Z
DTSTART;VALUE=DATE-TIME;TZID=Europe/Berlin:????
DTEND;VALUE=DATE-TIME;TZID=Europe/Berlin:????
DESCRIPTION;LANGUAGE=de-DE:????
LOCATION;LANGUAGE=de-DE:????
SUMMARY;LANGUAGE=de-DE:????
URL:https://????
UID:????
CONTACT;LANGUAGE=de-DE:????
END:VEVENT
"""

      vcal_stat = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Calendar Templates//Event Template//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
REFRESH-INTERVAL;VALUE=DURATION:P1W
COLOR:crimson
X-WR-CALNAME:GöKB Kalender
X-WR-CALDESC:Veranstaltungskalender gesammelt durch das Göttinger Klimabündnis
URL:https://goettinger-klimabuendnis.de/event/
SOURCE;VALUE=URI:https://goettinger-klimabuendnis.de/event/
NAME;LANGUAGE=de-DE:GöKB Kalender
DESCRIPTION;LANGUAGE=de-DE:Veranstaltungskalender gesammelt durch das Göttinger Klimabündnis
"""
      vtimezone = """

BEGIN:VTIMEZONE
TZID:Europe/Berlin
TZURL:http://tzurl.org/zoneinfo-outlook/Europe/Berlin
X-LIC-LOCATION:Europe/Berlin

BEGIN:DAYLIGHT
TZNAME:CEST
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT

BEGIN:STANDARD
TZNAME:CET
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD

END:VTIMEZONE
"""
      vcal_end = """
END:VCALENDAR
"""
      self.v_uuid = str(uuid.uuid4())
      vevent1 = self.v_modify(vevent,description,summary,location,dtstart,dtend,url,contact)
      
      
      self.vcal_entry = vcal_stat + "UID:" + self.v_uuid + vtimezone + vevent1 + vcal_end
      return
   
   def get_event(self):
      return self.vcal_entry
      
   def v_modify(self,vevent,description,summary,location,dtstart,dtend,url,contact):
      v_array = vevent.split("\n")
      v_array = self.v_line_mod(v_array,"DESCRIPTION",description)
      v_array = self.v_line_mod(v_array,"SUMMARY",summary)
      v_array = self.v_line_mod(v_array,"LOCATION",location)
      v_array = self.v_line_mod(v_array,"DTSTART",dtstart)
      v_array = self.v_line_mod(v_array,"DTEND",dtend)
      v_array = self.v_line_mod(v_array,"URL",url)
      v_array = self.v_line_mod(v_array,"CONTACT",contact)
      v_array = self.v_line_mod(v_array,"UID",self.v_uuid)
      vevent1 = ""
      for line in v_array:
         vevent1 += line + "\n"
      return vevent1

   def v_line_mod(self,varray,prefix,val):
      k = 0
      for line in varray:
         if line.startswith(prefix):
            splitline = line.split(":")
            if val != "":
               newline = splitline[0] + ":" + val
            else:
               newline = ""
            varray[k] = newline
         k += 1
      return varray

#####################################

class event():

    def __init__(self):
        self.months = [
            "Januar",
            "Februar",
            "März",
            "April",
            "Mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember"
        ]
    
    def get_event_from_file(self,file=None):
        date = today = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        edate = ""
        etime = datetime.now().strftime('%H:%M')
        title = ""
        subtitle = ""
        url = ""
        place = ""
        author = ""
        locURL = ""
        header = False
        image = ""
        text = ""
        self.file = file
        if file != None:
            fd = open(file)
            pre_text = ""
            for line in fd.readlines():
                if line.startswith("Kalenderdatei:"):
                   continue
                if line[:-1] == "---":
                    if header == False:
                        header = True
                        continue
                    else:
                        header = False
                        continue
                elif  header == True: # and line[:-1] != "":
                    print (line[:-1])
                    Type = line[:-1].split(":")[0]
                    Value = line[:-1].split(":")[1]
                    for item in line[:-1].split(":")[2:]:
                        Value += ":" + item
                    if Type == "date" :
                        date = Value.split("T")[0].strip().strip('"')
                        ttime = Value.split("T")[1].strip().strip('"').split(":")
                        time = ttime[0] + ":" + ttime[1] + ":00"
                    if Type == "etime" :
                        edate = Value.split("T")[0].strip().strip('"')
                        ettime = Value.split("T")[1].strip().strip('"').split(":")
                        etime = ettime[0] + ":" + ettime[1] + ":00"
                    if Type == "title" :
                        title = Value.strip().strip('"')
                    if Type == "subtitle" :
                        subtitle = Value.strip().strip('"')
                    if Type == "url" :
                        url = Value.strip().strip('"')
                    if Type == "place" :
                        place = Value.strip().strip('"')
                    if Type == "author" :
                        author = Value.strip().strip('"')
                    if Type == "locURL" :
                        locURL = Value.strip().strip('"')
                    if Type == "image" :
                        image = Value.strip().strip('"')
                else:
                    pre_text += line
            pre_text = pre_text.strip()
            
            title_line_mark = False
            subtitle_line_mark = False
            text = ""
            for line in pre_text.split("\n"):
                if line.startswith(title):
                    title_line_mark = True
                    continue
                elif title_line_mark and line.startswith("====="):
                    title_line_mark = False
                    continue
                elif line.startswith(subtitle):
                    subtitle_line_mark = True
                    continue
                elif subtitle_line_mark and line.startswith("-----"):
                    subtitle_line_mark = False
                    continue
                elif not ( line.startswith("Mehr Informationen beim [Veranstalter]") or line.startswith("**Veranstaltung:")):
                            text += line + "\n"
        text = "\n" + text.strip() + "\n"
        print("#########",text)

        cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : url, "place" : place, "author" : author, "locURL" : locURL, "image" : image }
        return cont

    def get_next_recurring_event(self,cont,date):
        cont["date"] = date
        Time = cont["time"]
        Place = cont["place"]
        curr_events = {}
        curr_events[date + "_" + Time +  "_" + Place.replace(" ","").replace(",","")] = cont        
        return curr_events

    def get_new_event(self,cont):
        
        print ("Datum (" + cont["date"] + ")")
        Date = sys.stdin.readline()[:-1]
        if Date == "":
            Date = cont["date"]
        UTCplus = self.get_UTC(Date)
        if self.file != None:
            print ("Weitere Angaben ändern? (J|n)")
            ans = sys.stdin.readline()[:-1]
        else:
            ans = "j"
        if ans.lower() != "n":
            time = cont["time"].split(":")[0] + ":" + cont["time"].split(":")[1]
            print ("Uhrzeit: (" + time + ")" )
            Time =  sys.stdin.readline()[:-1]
            if Time == "":
                Time = time + ":00+" + UTCplus
            elif len(Time.split(":")) != 2:
                print ("Ungültige Zeit")
                sys.exit(1)
            else:
                Time += ":00+" + UTCplus
            etime = str(int(Time.split(":")[0])+2) + ":" + Time.split(":")[1]
            print ("Uhrzeit Ende: (" + etime + ")" )
            eTime =  sys.stdin.readline()[:-1]
            if eTime == "":
                eTime = etime + ":00+" + UTCplus
            elif len(eTime.split(":")) != 2:
                print ("Ungültige Zeit")
                sys.exit(1)
            else:
                eTime += ":00+" + UTCplus            
            print ("Titel (" + cont["title"] + ")" )
            Title = sys.stdin.readline()[:-1]
            if Title == "":
                Title = cont["title"]
            while Title[-1] == ".":
                Title = Title[:-1]
            print ("Untertitel (" + cont["subtitle"] + ")")
            Subtitle =  sys.stdin.readline()[:-1]
            if Subtitle == "":
                Subtitle = cont["subtitle"]
            print ("URL (" + cont["locURL"] + ")")
            LocURL =  sys.stdin.readline()[:-1]
            if LocURL == "":
                try:
                    LocURL = cont["locURL"]
                except:
                    LocURL = ""
            print ("Ort (" + cont["place"] + ")")
            Place =  sys.stdin.readline()[:-1]
            if Place == "":
                Place = cont["place"]
            print ("Author (" + cont["author"] + ")")
            Author =  sys.stdin.readline()[:-1]
            if Author == "":
                Author = cont["author"]
            print ("Banner-Bild (" + cont["image"] + ")")
            dirlist = os.listdir(homeDir + "/static" + banner_dir)
            dirlist.sort()
            for file in dirlist:
                if file.startswith("20"):
                    print(file)
            print ("/usr/bin/gwenview " + homeDir + "/static" + banner_dir)
            # out, err = sysCommand("/usr/bin/gwenview " + homeDir + "/static" + banner_dir)
            Image = sys.stdin.readline()[:-1]
            if Image == "":
                 Image = cont["image"]
            else:
                 Image = banner_dir + "/" + Image
            print ("den Text ändern? (j|N)")
            ans = sys.stdin.readline()[:-1]
            if ans.lower() == "j":  
                Text = ""
                for line in sys.stdin.readlines():
                    Text += line
            else:
                Text = cont["text"]
        else:
            Time =  cont["time"] + "+" + UTCplus
            eTime =  cont["etime"] + "+" + UTCplus
            Title = cont["title"]
            Subtitle = cont["subtitle"]
            LocURL = cont["locURL"]
            Place = cont["place"]
            Author = cont["author"]
            Image = cont["image"]
            Text = cont["text"]
            print("#########",Text)
    
        url = "/" + Date.split("T")[0].replace("-","/") + "/" + Time.replace(":","/") + "/"
    
        cont = {"date" : Date, "time" : Time, "etime" : eTime, "title" : Title, "subtitle" : Subtitle, "text" : Text, "url" : url, "place" : Place, "author" : Author, "locURL" : LocURL, "image" : Image }
        curr_events = {}
        curr_events[str(Date) + "_" + Time +  "_" + Place.replace(" ","").replace(",","")] = cont
        return curr_events
            
    def get_UTC(self,date):
        UTCplus = "01:00"
        self.month = date.split("-")[1]
        if self.month > "03" and self.month < "11":
            UTCplus = "02:00"
        return UTCplus
        
    def get_publish_date(self,date_str, publish_delta):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        publish_date = date - timedelta(days=publish_delta)
        if today > publish_date:
            publish_date = today
        return publish_date.strftime("%Y-%m-%d")
    
    def normalize_date(self,Date):
        ret = ""
        if len(Date.split("-")) == 3:
            date_fields = Date.split("-")
            try:
                date_fields[0] =  "{:02d}".format(int(date_fields[0]))
                date_fields[1] =  "{:02d}".format(int(date_fields[1]))
            except:
                print ("Ungültiges Datum")
                sys.exit(1)
            if len(date_fields[0]) == 4 and len(date_fields[1]) == 2 and len(date_fields[2]) == 2 :
                ret = Date
            elif len(date_fields[0]) == 2 and len(date_fields[1]) == 2 and len(date_fields[2]) == 2 :
                ret = date_fields[2] + "-" + date_fields[1] + "-" + date_fields[0]   
            else:
                print ("Ungültiges Datum")
                sys.exit(1)
        if len(Date.split(".")) == 3:
            date_fields = Date.split(".")
            try:
                date_fields[0] =  "{:02d}".format(int(date_fields[0]))
                date_fields[1] =  "{:02d}".format(int(date_fields[1]))
            except:
                print ("Ungültiges Datum")
                sys.exit(1)
            if len(date_fields[0]) == 2 and len(date_fields[1]) == 2 and len(date_fields[2]) == 2 :
                ret = "20" + date_fields[2] + "-" + date_fields[1] + "-" + date_fields[0]
            elif len(date_fields[0]) == 2 and len(date_fields[1]) == 2 and len(date_fields[2]) == 4 :
                ret = date_fields[2] + "-" + date_fields[1] + "-" + date_fields[0]
            else:
                print ("Ungültiges Datum")
        if len(Date.split(" ")) == 3:
            date_fields = Date.replace(".","").split(" ")
            if len(date_fields[0]) <= 2 and len(date_fields[1]) <= 2:
                try:
                    date_fields[0] =  "{:02d}".format(int(date_fields[0]))
                    date_fields[1] =  "{:02d}".format(int(date_fields[1]))
                except:
                    print ("Ungültiges Datum")
                    sys.exit(1)
                if len(date_fields[2]) < 4:
                    try:
                        date_fields[2] = "20" +  "{:02d}".format(int(date_fields[2]))
                    except:
                        print ("Ungültiges Datum")
                        sys.exit(1)
                ret = date_fields[2] + "-" + date_fields[1] + "-" + date_fields[1]
            elif len(date_fields[0]) <= 2 and len(date_fields[1]) > 2 and len(date_fields[2]) <= 4 :
                try:
                    date_fields[1] =  "{:02d}".format(self.months.index(date_fields[1])+1)
                except:
                    print ("Ungültiges Datum")
                    sys.exit(1)
                ret = date_fields[2] + "-" + date_fields[1] + "-" + date_fields[0]
            else:
                print ("Ungültiges Datum")
        return ret
    
    def text2ascii(self,text):
        umlaute = {
            "ä" : "ae",
            "ö" : "oe",
            "ü" : "ue",
            "Ä" : "AE",
            "Ö" : "OE",
            "Ü" : "UE",
            "ß" : "ss"
        }
        
        for char in umlaute:
            text = text.replace(char,umlaute[char])
        ttext = ""
        for char in text:
            if char in "abcdefghijklmnopqrstuvwxyz_:.[]{}() -ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                ttext += char
        return ttext
    
    
    def pretty_date(self,date,time):
        date_parts = date.split("-")
        time_parts = time.split(":")
        return date_parts[2] + ". " + self.months[int(date_parts[1])-1] + " " + date_parts[0] + ", " + time_parts[0] + ":" + time_parts[1]
    
               
    def dict2eventMD(self,ev_dict,publish_delta=100,outDir=outDir):
    
        for item in ev_dict:
            dlist = str(ev_dict[item]['date']).split("-")
            tlist = str(ev_dict[item]['time']).split(":")
            title_str = self.text2ascii(str(ev_dict[item]['title'])).replace(" ","_").replace(",","").replace(":","").replace(";","").replace("[","").replace("]","").replace("!","").replace("/","").replace(".","").replace("?","")
            outFN = outDir + "/" + dlist[0] + "-" + dlist[1] + "-" + dlist[2] + "_" + tlist[0] + tlist[1] + "_" + title_str + ".md"
            outFF = open(outFN, "w")
            outstr = "---\n" + \
            "layout:        events\n" + \
            "title:         \"" + str(ev_dict[item]['title']).replace('"',"'") + "\"\n" + \
            "subtitle:      \"" + str(ev_dict[item]['subtitle']).replace('"',"'") + "\"\n" + \
            "date:          " + str(ev_dict[item]['date']) + "T" +  str(ev_dict[item]['time']) + "\n" + \
            "etime:         " + str(ev_dict[item]['date']) + "T" +  str(ev_dict[item]['etime']) + "\n" + \
            "publishdate:   " + self.get_publish_date(ev_dict[item]['date'],publish_delta) + "T00:00:00+01:00\n" + \
            "author:        \"" + str(ev_dict[item]['author']) + "\"\n" + \
            "place:         \"" + self.text2ascii(str(ev_dict[item]['place'])) + "\"\n" + \
            "URL:           \"/" + dlist[0] + "/" + dlist[1] + "/" + dlist[2] + "/" + tlist[0] + "/" + tlist[1] + "/" + title_str + "\"\n" + \
            "locURL:        \"" + str(ev_dict[item]['locURL']) + "\"\n" + \
            "image:         \"" + str(ev_dict[item]['image']) + "\"\n" + \
            "---\n" + \
            "\n**Veranstaltung: " + self.pretty_date(ev_dict[item]['date'],ev_dict[item]['time']) + " Uhr, " + str(ev_dict[item]['place']) + "**\n" \
            "\n" + str(ev_dict[item]['title']) + "\n===========\n"
            if str(ev_dict[item]['subtitle']) != "":
                outstr += "\n" + str(ev_dict[item]['subtitle']) + "\n-----------\n"
            outstr += "\n\nKalenderdatei: [📆](/ics/" + dlist[0] + "-" + dlist[1] + "-" + dlist[2] + "_" + tlist[0] + "-" + tlist[1] + "_" + title_str.lower() + ".ics)\n\n"
            if str(ev_dict[item]['text']) != "":
                outstr += str(ev_dict[item]['text']) + "\n"
            if str(ev_dict[item]['locURL']) != "":
                outstr += "\nMehr Informationen beim [Veranstalter](" + str(ev_dict[item]['locURL']) + ")\n"
            print (outstr)
            outFF.write(outstr)
            outFF.close()
        return outFN


    def dict2eventICAL(self,ev_dict,outDir=outDir):
           
       for item in ev_dict:
          dlist = str(ev_dict[item]['date']).split("-")
          tlist = str(ev_dict[item]['time']).split(":")
          title_str = self.text2ascii(str(ev_dict[item]['title'])).replace(" ","_").replace(",","").replace(":","").replace(";","").replace("[","").replace("]","").replace("!","").replace("/","").replace(".","").replace("?","")
          outFN = icsDir + "/" + dlist[0] + "-" + dlist[1] + "-" + dlist[2] + "_" + tlist[0] + "-" + tlist[1] + "_" + title_str.lower() + ".ics"            
          outFF = open(outFN, "w")
          descr = ev_dict[item]['title'] + "\\n\\n" + ev_dict[item]['subtitle'] + "\\n\\n" + ev_dict[item]['text'].replace("\n","\\n")
          # sumry_ptr = descr[:124].rfind(". ")
          # sumry = descr[0:sumry_ptr+1] + " ..."
          sumry = ev_dict[item]['title'] + ", " + ev_dict[item]['subtitle']
          dt_start = ev_dict[item]['date'].replace("-","") + "T" + ev_dict[item]['time'].replace(":","")[:6] 
          dt_end = ev_dict[item]['date'].replace("-","") + "T" + ev_dict[item]['etime'].replace(":","")[:6]
          loc = ev_dict[item]['place']
          dt_contact = ""
          dt_rel_url = dlist[0] + "/" + dlist[1] + "/" + dlist[2] + "/" + tlist[0] + "/" + tlist[1] + "/" + title_str.lower()
          dt_url = "https://goettinger-klimabuendnis.de/" + dt_rel_url

            
          Vcal = vcal(description=descr,summary=sumry,location=loc,dtstart=dt_start,dtend=dt_end,url=dt_url,contact=dt_contact)
          print(Vcal.get_event())
          outFF.write(Vcal.get_event())
          outFF.close()
       return dt_rel_url


    def prepare_events(self,file=None,recurring=None):
        ans = "Yes"
        inFN = file
        while len(ans) > 0 and ans[0].lower() == "y":
            evt = self.get_event_from_file(file=inFN)
            if recurring == None:
                new_evt = self.get_new_event(evt)
            else:
                nextDate = recurringDates(evt["date"],sys.argv[2]).nextDate
                rDate = nextDate.strftime('%Y-%m-%d')
                new_evt = self.get_next_recurring_event(evt,rDate)
            self.dict2eventICAL(new_evt)
            outFN = self.dict2eventMD(new_evt, publish_delta=publish_delta)
            print( "Written to: " + outFN)
            print ("#######################################")
            print("use output file for next event [y|N]:")
            ans = sys.stdin.readline()[:-1]
            inFN = outFN
            
##########################
if __name__ == '__main__':

    publish_delta = 100

    Event = None
    Vcal = vcal(description="Test Veranstaltung ausführlich",summary="Test Veranstaltung ...",location="Test Ort",dtstart="20250208T140000",dtend="20250208T150000",url="https://goettinger-klimabuendnis.de/event/",contact="a.b@c.de")
    # sys.exit(0)
    Event = event()
    if len(sys.argv) == 1:
        Event.prepare_events()
    elif len(sys.argv) == 2:
        Event.prepare_events(file=sys.argv[1])
    elif len(sys.argv) == 3:
        Event.prepare_events(file=sys.argv[1], recurring=sys.argv[2])
    else:
        print ("Usage:", sys.argv[0], "reference_file [date_offset]")
        sys.exit(1)
        
     
