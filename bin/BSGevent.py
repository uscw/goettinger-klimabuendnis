from datetime import date, datetime, timezone, timedelta
#from event
import event

class eventBSG():

    months = [ "Januar",
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
    
    days = [ "Sonntag",
             "Montag",
             "Dienstag",
             "Mittwoch",
             "Donnerstag",
             "Freitag",
             "Samstag"
            ]

    def __init__(self):
        self.reset_event()

    def reset_event(self):    
        self.date = self.today = datetime.now().strftime('%Y-%m-%d')
        self.time = datetime.now().strftime('%H:%M')
        self.edate = ""
        self.etime = datetime.now().strftime('%H:%M')
        self.title = ""
        self.subtitle = ""
        self.url = ""
        self.place = ""
        self.author = "Biologische Schutzgemeinschaft Göttingen e.V. (BSG)"
        self.locURL = "http://www.biologische-schutzgemeinschaft.de/programm.html"
        self.header = False
        self.image = "/img/banner/2021-02-25-Göttingen-Holzbiene.jpg"
        self.text = """
Wir bitten um Anmeldung zu den Veranstaltungen unter mail@biologische-schutzgemeinschaft.de

Biologische Schutzgemeinschaft Göttingen e.V. (BSG)
-- Vereinigung für Natur- und Umweltschutz --

GUNZ, Geiststraße 2, 37073 Göttingen (Bürozeiten: Jeden Mittwoch, 16-18 Uhr)
"""
        self.cont = { "date" : self.date,
                 "time" : self.time,
                 "etime" : self.etime,
                 "title" : self.title,
                 "subtitle" : self.subtitle,
                 "text" : self.text,
                 "url" : self.url,
                 "place" : self.place,
                 "author" : self.author,
                 "locURL" : self.locURL,
                 "image" : self.image
                }
        return self.cont
        
    
    def get_event_from_file(self,file=None):
        IP = open(file,"r")
        month = ""
        out_data = self.cont

        lastline = ""
        isEvent = False
        evt_txt = None
        txt_cont = []
        # get event blocks
        for line in IP.readlines():
            line = line[:-1]
            if line == "":
                isEvent = False
                continue
            if lastline.strip() in ["Sommerprogramm", "Winterprogramm"]:
                self.year = line.split()[-1:][0]
                print ("Year: ", self.year)
            elif line.strip().startswith("Fortsetzung " + month):
                isEvent = False
                # print (" found: Fortsetzung " + month)
                continue
            elif line.split()[0] == "Sonstiges":
                isEvent = False
            elif line.strip().split()[0] in self.days:
                isEvent = True
                if evt_txt != None:
                    txt_cont.append(evt_txt)
                evt_txt = [ line[len(line.strip().split()[0])+1:].strip() ]
            elif isEvent:
                if lastline.strip().split()[0] in self.days:
                    evt_txt.append(line.strip().split()[0])
                    evt_txt.append(line.strip()[len(line.strip().split()[0])+1:].strip())
                    #evt_txt.append(line.strip())
                else:
                    evt_txt.append(line.strip())
            lastline = line
        return txt_cont

    def get_date(self,item):
        # get date
        parts = item[1].split()[0].split(".")
        # txt_cont[item] = item[1][len(item[1].split()[0])+1:].strip()
        for i in range(len(parts)):
            if len(parts[i]) == 1:
                parts[i] = "0" + parts[i]
        d = parts[0]
        m = parts[1]
        y = self.year
        self.cont["date"] = y + "-" + m + "-" + d
        return self.cont["date"]
    
    def get_time_and_place(self,item):
        # get time:
        t_str = ""
        t_alt = ""
        lastword = ""
        llastword = ""
        k = 0
        for subitem in item:
            # cont = self.reset_event()
            words = subitem.replace("  "," ").replace("Treffen:","Treffen: ").split()
            for word in words:
                if word.strip().replace(",","").replace(";","").replace(".","").replace("!","").replace(":","") == "Uhr":
                    self.used_items.append(k)
                    t_alt = lastword
                    if llastword == "Treffen:":
                        t_str = lastword.replace(",","").replace(";","").replace("!","")
                    place = subitem[subitem.find("Uhr") + 4:].strip()
                llastword = lastword
                lastword = word
            if t_str == "" and t_alt != "":
                t_str = t_alt
            if subitem.strip().lower().startswith("leitung:"):
                subsubtitle2 = subitem
                self.used_items.append(k)
            k += 1
        t_str = t_str.replace(".",":")
        if len(t_str) == 1:
            t_str = "0" + t_str + ":00"
        elif len(t_str) == 2:
            t_str = t_str + ":00"
        elif len(t_str) == 4:
            t_str = "0" + t_str
        if len(t_str) != 5:
            print("Error: Time not found in", item)
            t_str = ""
            return t_str
        UTCplus = event.event().get_UTC(self.date)
        self.cont["time"] = t_str + ":00+" + UTCplus
        # get etime
        if t_str.split(":")[0] == "22":
            etime = "00:00"
        elif t_str.split(":")[0] == "23":
            etime = "01:00"
        else:
            etime_h = str(int(t_str.split(":")[0]) + 2 )
            if len(etime_h) == 1:
                etime_h = "0" + etime_h
            etime = etime_h + ":" + t_str.split(":")[1]
        self.cont["etime"] = etime + ":00+" + UTCplus

        
        self.cont["place"] = place
        return self.cont["time"]
    
    def get_titles(self, item):
        # get title and subtitle
        subsubtitle2 = ""
        if item[0].strip().lower().startswith("jahreshauptversammlung"):
            return None, None
        if item[0].strip().lower().startswith("vortrag"):
            title = "Vortrag: " + item[2]
            subtitle = "Eine Veranstaltung der Biologischen Schutzgemeinschaft e.V. Göttingen"
            subsubtitle1 = item[0]
        else:
            title = item[0]
            subtitle = "Eine Veranstaltung der Biologischen Schutzgemeinschaft e.V. Göttingen"
            subsubtitle1 = item[2]
        self.used_items.append(0)
        self.used_items.append(1)
        self.used_items.append(2)
        if subsubtitle1 == subsubtitle2:
            subsubtitle2 = ""
        if subsubtitle2.startswith("Leitung:"):
            subsubtitlet = subsubtitle2
            subsubtitle2 = subsubtitle1
            subsubtitle1 = subsubtitlet
        self.cont["title"] = title
        self.cont["subtitle"] = subtitle
        return subsubtitle1, subsubtitle2
        
    def get_text(self,item,subsubtitle1,subsubtitle2):
        # if subsubtitle1.strip() != "":
        #     text = "\n**" + subsubtitle1 + "**\n\n"
        # if subsubtitle2.strip() != "":
        #     text += subsubtitle2 + "\n\n"
        subtext = self.cont["text"]
        # self.cont["text"] = self.cont["title"] + "\n=============\n\n"
        self.cont["text"] = subsubtitle1 + "\n-------------\n\n"
        if subsubtitle2.strip() != "":
            self.cont["text"] +=  "\n**" + subsubtitle2 + "**\n\n"
        k = 0
        for subitem in item:
            if k not in self.used_items:
                self.cont["text"] += subitem + "\n\n"
            k += 1
        self.cont["text"] += subtext
        
    def get_event_components(self,txt_cont):
        # get event components from event blocks
        evt_dict = {}
        for item in txt_cont:
            self.used_items = []
            self.reset_event()
            print(">>>> ",item)
            self.get_date(item)
            print ("date", self.cont["date"] )
            self.get_time_and_place(item)
            if self.cont["time"] == "":
                continue # not an event found !?
            subsubtitle1, subsubtitle2 = self.get_titles(item)
            if subsubtitle1 == None:
                continue
            self.cont["url"] = "/" + self.cont["date"].replace("-","/") + "/" + self.cont["time"].replace(":","/") + "/"
            self.get_text(item,subsubtitle1,subsubtitle2)

            # print ("time",self.cont["time"])
            # print ("etime",self.cont["etime"])
            # print ("place",self.cont["place"])
            # print ("title",self.cont["title"])
            # print ("subtitle",self.cont["subtitle"])
            # print ("text", self.cont["text"])
            print (self.cont)
            evt_dict[str(self.cont["date"]) + "_" + self.cont["time"] +  "_" + self.cont["place"].replace(" ","").replace(",","")] = self.cont
            
            #evt_list.append(self.cont)
            
        return evt_dict
##########################
if __name__ == '__main__':

    ProgFile="/home/uschwar1/Downloads/Programm.txt"
    publish_delta = 100

    EventBSG = eventBSG()
    txt_cont = EventBSG.get_event_from_file(file=ProgFile)
    evt_dict = EventBSG.get_event_components(txt_cont)
    print (evt_dict)

    Evt = event.event()
    # print (Evt.get_new_event(evt_list[0]))
    eFN = Evt.dict2eventMD(evt_dict,publish_delta=200,outDir="/tmp/event")
#    print (eFN)
