import sys
from datetime import date, datetime, timezone, timedelta
#from event
import event

usage = """
Der ADFC Kreisverband Göttingen bietet von April bis Oktober Radtouren an.


Input: Text file as output from pdftotext from Programm.pdf not sufficient
It needs to be prepared: Typical program item:

Samstag
28.9.

Naturschutz praktisch: Quellsumpf Scheden
Vorkommen von Gelb-Seggen, Herbstzeitlose, Teufelsabbiss
Breitblättrigem Knabenkraut und Fuchs' Knabenkraut.
Treffen: 9 Uhr, Göttinger Umwelt- und Naturschutzzentrum, Geiststr. 2

"""

class eventADFC():

    months_full = [ "Januar",
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

    months = [ "Jan.",
               "Feb.",
               "Mär.",
               "Apr.",
               "Mai",
               "Juni",
               "Juli",
               "Aug.",
               "Sep.",
               "Okt.",
               "Nov.",
               "Dez."
              ]

    days = [ "Sonntag",
             "Montag",
             "Dienstag",
             "Mittwoch",
             "Donnerstag",
             "Freitag",
             "Samstag"
            ]

    level = {
        "sehr einfach" : """
**Gemütliche Tour** (G)

Für wen geeignet: ungeübte Radfahrer*innen  
Geschwindigkeit: langsam (unter 15 km/h)  
Strecke: ca. 20 – 40 km  
Steigungen: selten vorhanden, notfalls wird geschoben
""",
        "einfach" : """
**Leichtere Tour** (E)

Für wen: weniger Geübte und Kinder mit Ausdauer  
Geschwindigkeit: gemütlich (ca. 15 – 18 km/h)  
Strecke: ca. 30 – 60 km  
Steigungen: ab und an leichte vorhanden  
""",
        "mittel" : """
**Mittlere Tour** (M)

Für wen geeignet: geübte Radfahrer*innen  
Geschwindigkeit: etwas flotter (ca. 19 – 21 km/h)  
Strecke: ca. 40 – 70 km  
Steigungen: öfter vorhanden, meist leichterer Art oder wenige stärkere
""",
        "schwer" : """
**Anspruchsvolle Tour** (A)

Für wen geeignet: Radfahrer*innen mit Ausdauer  
Geschwindigkeit: flott (ca. 22 – 25 km/h)  
Strecke: ca. 60 – 100 km  
Steigungen: öfter vorkommend, zum Teil schon stärker  
""",
        "sehr schwer" : """
Sportliche Tour (S)

Für wen: sportliche Radfahrer*innen mit guter Ausdauer  
Geschwindigkeit: schnell (über 25 km/h)  
Strecke: ab 90 km  
Steigungen: häufig vorhanden  
"""
    }
    
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
        self.author = "Allgemeiner Deutscher Fahrrad-Club (ADFC), Kreisverband Göttingen e.V."
        self.locURL = "https://goettingen.adfc.de/"
        self.header = False
        self.image = "/img/banner/2023-03-17-KidicalMass.jpg"
        self.text = """
Ausführliche Informationen zu den hier beschriebenen Touren
des ADFC und ggf. zur Anmeldung gibt es im ADFC-Tourenportal: 

https://touren-termine.adfc.de

Allgemeiner Deutscher Fahrrad-Club Kreisverband Göttingen e. V.  
Geiststraße 2  
37073 Göttingen  
https://goettingen.adfc.de/
(Bürozeiten: Mittwochs, 19.00 – 20.00 Uhr)
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
        Month = ""
        out_data = self.cont

        lastline = ""
        isEvent = False
        evt_txt = None
        txt_cont = []
        txt_subcont = []
        # get event blocks
        for line in IP.readlines():
            line = line[:-1]
            if line == "":
                continue
            elif line == "image":
                if txt_subcont != []:
                    txt_cont.append(txt_subcont)
                txt_subcont = []
            else:
                txt_subcont.append(line)
        return txt_cont
    
    def get_date_time(self,item):
        dt_fields = item[1].split()
        # get time:
        t_field = dt_fields[4].zfill(5)
        e_field = str(int(dt_fields[4].split(":")[0]) + 4) + ":" + dt_fields[4].split(":")[1]
        d_field = dt_fields[1].replace(".","").zfill(2)
        m_field = str(self.months.index(dt_fields[2]) + 1).zfill(2)
        y_field = dt_fields[3]
        date = y_field + "-" + m_field  + "-" + d_field
        return date, t_field, e_field 
    
        
    def get_text(self,item):
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
            if len(item) != 5:
                print (item)
            else:
                 evt_dict["title"] = item[2]
                 evt_dict["subtitle"] = item[0]
                 evt_dict["text"] = item[3] # self.get_text(item)
                 evt_dict["date"], evt_dict["time"], evt_dict["etime"] = self.get_date_time(item)
                 #evt_dict["url"] = "123",
                 #evt_dict["place"] = self.get_place(item),
                 #evt_dict["author"] = self.get_author(item),
                 #evt_dict["locURL"] = self.locURL,
                 #evt_dict["image"] = self.image
            
        return evt_dict

    
##########################
if __name__ == '__main__':

    ProgFile="/home/uschwar1/Downloads/ADFC_S2024.txt"
    if len(sys.argv) < 2:
        print ("Usage: " + sys.argv[0] + " programm_file.txt\n\n")
        # sys.exit(1)
        # use default
    else:
        ProgFile = sys.argv[1]
    EventADFC = eventADFC()
    txt_cont = EventADFC.get_event_from_file(file=ProgFile)
    evt_dict = EventADFC.get_event_components(txt_cont)
    print (evt_dict)
    sys.exit(0)
    Evt = event.event()
    # print (Evt.get_new_event(evt_list[0]))
    # writes event files into directory /tmp/event
    eFN = Evt.dict2eventMD(evt_dict,publish_delta=200,outDir="/tmp/event")
    # print (eFN)

    
