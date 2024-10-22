import sys
import mechanicalsoup
import string
import csv
from datetime import date

class posts:

    def __init__(self):
        self.baseurl = "file:///home/uschwar1/ownCloud/AC/python/xmpls/events/downloads/goest_news20190513.html"
        self.baseurl = "http://www.goest.de/news.htm"
        self.today = date.today()
        self.Day = self.today.strftime("%d")
        self.Month = self.today.strftime("%m")
        self.Year = self.today.strftime("%Y")
        try:
            self.current_posts
        except:
            self.current_posts = {}
        url = self.baseurl
        self.get_posts(url, self.current_posts, self.Year,self.Month,self.Day)
        return self.current_posts

    def get_posts(self,url,curr_events,year,month,day):

        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1',
        )
        browser.open(url)
        page = browser.get_current_page()
        tables = page.findAll('table')

        for table in tables:
            for paragraph in table.findAll('p'):
                try:
                    h2=paragraph.find('br').previous_sibling.replace("\n","").replace("\r","")
                    #h3=paragraph.find('br').previous_sibling.text.replace("\n","")
                    print (h2)
                    #print (h3)
                except:
                    continue
                print ("\n")
        return curr_events

##########################
if __name__ == '__main__':
    post = posts()
    print (evt.current_posts)

    
