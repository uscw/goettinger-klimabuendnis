import sys
import mechanicalsoup
import string
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "http://www.lumiere.de/texte/kinderkino.htm"
        self.organizer = "Lumiere Kinderkino"
        self.locationICON = "lumiere-icon.png"
        self.locationIMG = "lumiere-img.jpg"
        self.locationURL = "http://www.lumiere.de/"
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test/"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        # (year, month) = divmod(self.today.month, 12)
        # self.nextMonth = self.today.replace(year=self.today.year+year, month=month+1, day=1)
        # self.NextMonth = self.nextMonth.strftime("%m")
        # self.current_events = self.get_curr_events(self.today.year,self.today.month,self.today.day)

        (year, month) = divmod(self.today.month, 12)
        self.Month = str(month)
        self.Year = str(int(self.Year) + year)
        self.current_events = self.get_curr_events()
        # (year, month) = divmod(self.today.month + 1, 12)
        # self.Month = str(month)
        # self.Year = str(int(self.Year) + year)
        # self.current_events = self.get_curr_events()

        

    def get_curr_events(self):

        try:
            self.current_events
        except:
            self.current_events = {}

        #get main page
        url = self.baseurl # + "index.html"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
            
        return self.current_events

    def get_events(self,url,current_events,year,month,day):

        items_visited = {}
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        )
        page = browser.get_current_page()
        
        dates = page.findAll("p", {'class':'title'} )
        for Date in dates:
            nextNode = Date
            datestr = Date.text
            try:
                Day = datestr.split(" ")[1].split(".")[0]
                Month = datestr.split(" ")[1].split(".")[1]
            except:
                continue
            if len(Day) == 1:
                Day = "0" + Day 
            if len(Month) == 1:
                Month = "0" + Month
            date = str(year) + "-" + Month + "-" + Day
            while True:
                try:
                    nextNode = nextNode.next_sibling
                    if nextNode.text == "" or nextNode.find("th") != None:
                        break
                    Time = nextNode.text.split("Uhr")[0].replace(" ","").split(".")
                    hour = Time[0]
                    if len(hour) == 1:
                        hour = "0" + hour
                    if len(Time) == 2:
                        minute = Time[1]
                    else:
                        minute = "00"
                    time = hour + ":" + minute
                except:
                    break
                try:
                    ref = nextNode.find("a")["href"].replace("../","")
                except:
                    None
                try:
                    visited = items_visited[ref]
                    text = visited["text"]
                    title = visited["title"]
                    subtitle = visited["subtitle"]
                except:
                    # get more info from reference
                    url = self.baseurl + ref
                    browser.open(url)
                    page = browser.get_current_page()
                    try:
                        title = page.find("h2").text
                    except:
                        title = ""
                    try:
                        subtitles = page.find("h3")
                    except:
                        subtitles = None
                    if subtitles != None:
                        stlist = str(subtitles).replace("<h3>","").replace("</h3>","").split("<br/>")
                        subtitle = stlist[0]
                        text = ""
                        for item in stlist[1:]:
                            text += item + ", " 
                        text += "Inhalt: " + page.find("p").text
                    
                    items_visited[ref] = { "title" : title, "subtitle" : subtitle, "text" : text }
                place = "Lumiere"
                etime = "" 
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : self.baseurl + ref, "place" : place, "organizer" : self.organizer, "locICON" : self.locationICON, "locIMG" : self.locationIMG, "locURL" : self.locationURL}
                current_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont
        
        return current_events
        #print len(dates), dates
        #print len(contents), contents
        

##########################
if __name__ == '__main__':
    evt = events()
    print(evt.current_events)
