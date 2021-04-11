import sys
import mechanicalsoup
import string
import csv
from datetime import date

class events:

    def __init__(self):
        self.baseurl = "https://www.exil-web.de"
        self.organizer = "Exil"
        self.locationICON = "Exil-live-music-club-icon.png"
        self.locationIMG = "Exil-live-music-club-img.jpg"
        self.locationURL = "http://www.exil-web.de/"
        
        # self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/test"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        (year, month) = divmod(self.today.month, 12)
        self.nextMonth = self.today.replace(year=self.today.year+year, month=month+1, day=1)
        self.NextMonth = self.nextMonth.strftime("%m")
        self.current_events = self.get_curr_events()


    def get_curr_events(self):
        
        try:
            self.current_events
        except:
            self.current_events = {}
        url = self.baseurl + "/index.php/ct-menu-item-5"
        # url = self.baseurl + "/dt_" + str(year) + str(month) + ".html"
        self.get_monthly_events(url, self.current_events, self.Year,self.Month,self.Day)
        return self.current_events

    def get_monthly_events(self,url,curr_events,year,month,day):

        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        )
        browser.open(url)
        page = browser.get_current_page()
        # <div class="eb-event-information row">
        for row in page.findAll('div',{'class':'eb-category-3 eb-event-container'}):
            txt = row.text
            try:
                #<meta itemprop="startDate" content="2019-04-21T21:00">
                #div class="eb-description-details clearfix
                #info = row.next_sibling
                date = row.find('div',{'class':'clearfix'}).text.replace("\n","").replace("\r","").replace("\t","")
                time = date[14:19]
                year = date[10:14]
                month= date[7:9]
                day  = date[4:6]
                date = year + "-" + month + "-" + day
            except:
                None
            try:
                desc = row.find('div',{'class':'eb-description-details clearfix'})
            except:
                None
            try:
                title = ""
                title = desc.find('br').previous_sibling.replace("\n","").replace("\r","").replace("\t","")
            except:
                None
            try:
                place = "EXIL Live Music Club"
                # place = row.find('div',{"itemprop","name"})
            except:
                None
            try:
                subtitle = ""
                for part in desc.findAll('br'):
                    if not part.next_sibling.startswith("Datum") and  not part.next_sibling.startswith("Support"):
                        subtitle += part.next_sibling + "; "
                subtitle = subtitle.replace("\n","").replace("\r","").replace("\t","")[:-2]
            except:
                None
            try:
                ref = ""
                ref = self.baseurl + row.find('a',{'class':'btn btn-default btn-primary'})["href"]
            except:
                None
            if title != "":
                etime = ""
                text = ""
                cont = {"date" : date, "time" : time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : ref, "place" : place, "organizer" : self.organizer, "locICON" : self.locationICON, "locIMG" : self.locationIMG, "locURL" : self.locationURL}
                ret = { str(date) + "_" + time +  "_" + place.replace(" ","") : cont }

                curr_events[str(date) + "_" + time +  "_" + place.replace(" ","")] = cont
        return curr_events

##########################
if __name__ == '__main__':
    evt = events()
    print (evt.current_events)

    
