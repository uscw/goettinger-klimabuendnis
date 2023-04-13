import sys
import mechanicalsoup
import string
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "http://www.junges-theater.de/"
        self.organizer = "Junges Theater"
        self.locationICON = "junges-theater-icon.png"
        self.locationIMG = "junges-theater-img.jpg"
        self.locationURL = "http://junges-theater.de"

        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/downloads/www.junges-theater.de/spielplan/index.html"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")

        
        (year, month) = divmod(self.today.month, 12)
        self.Month = str(month)
        self.Year = str(int(self.Year) + year)
        self.current_events = self.get_curr_events()
        (year, month) = divmod(self.today.month + 1, 12)
        self.Month = str(month)
        self.Year = str(int(self.Year) + year)
        self.current_events = self.get_curr_events()
         
    def get_curr_events(self):
        
        try:
            self.current_events
        except:
            self.current_events = {}
        url = self.baseurl + "spielplan/" + "?month=" + self.Month
        # url = self.baseurl + "jt-spielplan-month" + self.Month + ".html"
        self.get_events(url, self.current_events, self.Year,self.Month,self.Day)
            
        return self.current_events
    
    def get_events(self,url,curr_events,year,month,day):
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        )
        print(url)
        browser.open(url)
        page = browser.get_current_page()
        table = page.findAll("div",{"class":"row dark"})
        
        for row in table:#[1:]:
            divs0 = row.findAll("div")
            Day = divs0[0].text.split(".")[0][1:]
            Month = divs0[0].text.split(".")[1]
            date = str(year) + "-" + Month + "-" + Day
            divs00 = divs0[1].findAll("div")
            time = divs00[0].text.replace("Uhr","").strip()
            refpart = divs00[1].find("a", href=True)
            if refpart != None:
                ref = refpart["href"].replace("../","")
                title = refpart.text
            else:
                ref = url
                title = ""
                for item in divs00[1].findAll("span"):
                    title += item.text + " "
            subtitle = divs00[1].find("p").text[:-2]
            addRemark = title.lower().find("schulvorstellung(anmeldung erforderlich!)")
            if addRemark >= 0:
                subtitle += ", " + title[addRemark:]
                title = title[:addRemark]
            place = "Junges Theater"            
            text = ""
            etime = ""
            if title != "":
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" :  self.baseurl + ref, "place" : place, "organizer" : self.organizer, "locICON" : self.locationICON, "locIMG" : self.locationIMG, "locURL" : self.locationURL}
                curr_events[str(date) + "_" + time +  "_" + place.replace(" ","").split(",")[0]] = cont
            cont_csv = date + ";" + time + ";" + etime + ";" + title + ";" + subtitle + ";" + text + ";" +  ref + ";" +  place
            # print (cont_csv)
        return curr_events
        sys.exit(0)

        return curr_events



##########################
if __name__ == '__main__':
    evt = events()
    print (evt.current_events)

    
