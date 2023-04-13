import sys
import mechanicalsoup
import string
import csv
from datetime import date

class events:

    def __init__(self):
        self.organizer = "Theater im OP"
        self.baseurl = "http://www.thop.uni-goettingen.de/"
        self.locationICON = "thop-uni-goettingen-icon.png"
        self.locationIMG = "thop-uni-goettingen-img.jpg"
        self.locationURL = "http://www.thop.uni-goettingen.de/"

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
        url = self.baseurl + "kalender/index.php"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
            
        return self.current_events

    def get_events(self,url,current_events,year,month,day):

        items_visited = {}
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        )
        browser.open(url)
        page = browser.get_current_page()

        tables = page.findAll("table", {'class':'kalenderVorschau'})
        # print (tables)
        
        dates = tables[0].findAll("tr")#, {'id':'kalender'} )
        # print (dates)
        for Date in dates:
            nextNode = Date
            datestr = Date.text
            entries = nextNode.findAll("td")
            if len(entries) == 1:
                # print (entries)
                year =  entries[0].text.split()[1]
            elif len(entries) > 1:
                # print (entries)
                Date = entries[0].text
                Time = entries[1].text
    
                try:
                    Day = Date.split(".")[0]
                    Month = Date.split(".")[1]
                except:
                    continue
                if len(Day) == 1:
                    Day = "0" + Day 
                if len(Month) == 1:
                    Month = "0" + Month
                date = str(year) + "-" + Month + "-" + Day
                try:
                    Hour = Time.split(":")[0]
                    Min = Time.split(":")[1]
                except:
                    continue
                if len(Hour) == 1:
                    Houy = "0" + Hour
                if len(Min) == 1:
                    Min = "0" + Min
                time = Hour + ":" + Min
                
                
                while True:
                    title = ""
                    subtitle = ""
                    text = ""
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

                subtitle1 = entries[2].text
                title = entries[3].text
                if len(subtitle1) < 2:
                    try: 
                        stitle = title.split("- ")[1:]
                        subtitle1 = ""
                        for item in stitle:
                            subtitle1 += item + " "
                        title = title.split("- ")[0]
                    except:
                        none
                try:
                    ref = self.baseurl + entries[3].find("a")["href"].replace("../","")
                except:
                    ref = ""
                if ref != "":
                    try:
                        visited = items_visited[ref]
                        text = visited["text"]
                        title = visited["title"]
                        subtitle = visited["subtitle"]
                    except:
                        # get more info from reference
                        browser.open(ref)
                        page = browser.get_current_page()
                        ppage = page.find("table",{'class':'linie'})
                        try:
                            title = ppage.find("h1",{'class':'titelStueckAutor fontface'}).text
                        except:
                            None
                    try:
                        stitles = ppage.findAll("h3",{'class':'titelStueckAutor fontface'})
                        if len(stitles) > 1:
                            subtitle = stitles[1].text.replace("//", " ").replace("\n", ", ")
                            subtitle +=  stitles[0].text.replace("\n", " ")
                        else:
                            subtitle =  stitles[0].text.replace("//", " ").replace("\n", " ")                        
                    except:
                        None
                    try:
                        text = ppage.find("div").text.replace("\n","\n\n")
                    except:
                        text = ""
                subtitle += subtitle1
                subtitle = subtitle.strip()
                # if subtitles != None:
                #     stlist = str(subtitles).replace("<h3>","").replace("</h3>","").split("<br/>")
                #     subtitle = stlist[0]
                #     text = ""
                #     for item in stlist[1:]:
                #         text += item + ", " 
                #     text += "Inhalt: " + page.find("p").text
    
                items_visited[ref] = { "title" : title, "subtitle" : subtitle, "text" : text }
                place = entries[4].text
                etime = ""
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : self.baseurl + ref, "place" : place, "organizer" : self.organizer, "locICON" : self.locationICON, "locIMG" : self.locationIMG, "locURL" : self.locationURL}
    
                current_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont

        return current_events
        

##########################
if __name__ == '__main__':
    evt = events()
    print(evt.current_events)
