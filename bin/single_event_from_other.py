import os
import sys
from datetime import date, datetime, timedelta

locURL = {
    "Lumiere" : ["http://www.lumiere.de/","lumiere-icon.png"],
    "ThOP" : ["http://www.thop.uni-goettingen.de/","thop-uni-goettingen-icon.png"],
    "Literarisches Zentrum" : ["http://www.literarisches-zentrum-goettingen.de/","literarisches-zentrum-icon.png"],
    "Junges Theater" : ["http://junges-theater.de/","junges-theater-icon.png"],
    "Deutsches Theater" : ["https://www.dt-goettingen.de/","deutsches-theater-icon.png"],
    "EXIL" : ["http://www.exil-web.de/","Exil-live-music-club.png"]
    }

months = [
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

banner_dir = "static/img/banner"

def get_event(file=None):
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
    if file != None:
        fd = open(file)
        pre_text = ""
        for line in fd.readlines():
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
            elif not ( line.startswith("Mehr Informationen auf der [Webseite des Veranstalters]") or line.startswith("**Veranstaltung:")):
                        text += line + "\n"
    print("#########",text)

    print ("Datum (" + date + ")")
    Date = sys.stdin.readline()[:-1]
    if Date == "":
        Date = date
    UTCplus = "01:00"
    month = Date.split("-")[1]
    if month > "03" and month < "11":
        UTCplus = "02:00"
    print ("Weitere Angaben ändern? (J|n)")
    ans = sys.stdin.readline()[:-1]
    if ans.lower() != "n":
        print ("Uhrzeit: (" + time + ")" )
        Time =  sys.stdin.readline()[:-1]
        if Time == "":
            Time = time.split("+")[0] + ":00+" + UTCplus
        elif len(Time.split(":")) != 2:
            print ("Ungültige Zeit")
            sys.exit(1)
        else:
            Time += ":00+" + UTCplus
        print ("Uhrzeit Ende: (" + etime + ")" )
        eTime =  sys.stdin.readline()[:-1]
        if eTime == "":
            eTime = etime + ":00+" + UTCplus
        elif len(eTime.split(":")) != 2:
            print ("Ungültige Zeit")
            sys.exit(1)
        else:
            eTime += ":00+" + UTCplus            
        print ("Titel (" + title + ")" )
        Title = sys.stdin.readline()[:-1]
        if Title == "":
            Title = title
        print ("Untertitel (" + subtitle + ")")
        Subtitle =  sys.stdin.readline()[:-1]
        if Subtitle == "":
            Subtitle = subtitle
        print ("URL (" + locURL + ")")
        LocURL =  sys.stdin.readline()[:-1]
        if LocURL == "":
            LocURL = locURL
        print ("Ort (" + place + ")")
        Place =  sys.stdin.readline()[:-1]
        if Place == "":
            Place = place
        print ("Author (" + author + ")")
        Author =  sys.stdin.readline()[:-1]
        if Author == "":
            Author = author
        print ("Banner-Bild (" + image + ")")
        for file in os.listdir(banner_dir):
            print(file)
        Image =  sys.stdin.readline()[:-1]
        if Image == "":
             Image = image
        print ("den Text ändern? (j|N)")
        ans = sys.stdin.readline()[:-1]
        if ans.lower() == "j":  
            Text = ""
            for line in sys.stdin.readlines():
                Text += line
        else:
            Text = text
    else:
        Time = time.split("+")[0] + "+" + UTCplus
        eTime = time.split(":")[0] + ":" + etime.split(":")[1] + ":00+" + UTCplus
        Title = title
        Subtitle = subtitle
        LocURL = locURL
        Place = place
        Author = author
        Image = image
        Text = text
        print("#########",text)

    url = "/" + Date.split("T")[0].replace("-","/") + "/" + Time.replace(":","/") + "/"

    cont = {"date" : Date, "time" : Time, "etime" : eTime, "title" : Title, "subtitle" : Subtitle, "text" : Text, "url" : url, "place" : Place, "author" : Author, "locURL" : LocURL, "image" : Image }
    curr_events = {}
    curr_events[str(Date) + "_" + Time +  "_" + place.replace(" ","").replace(",","")] = cont
    return curr_events
        

# def get_event():
#     today = datetime.now().strftime('%Y-%m-%d')
#     print ("Datum (" + today + ")")
#     Date = sys.stdin.readline()[:-1]
#     Date = normalize_date(Date)
#     now = datetime.now().strftime('%H:%M')
#     print ("Uhrzeit: (" + now + ")" )
#     Time =  sys.stdin.readline()[:-1]
#     if Time == "":
#         Time = now
#     if len(Time.split(":")) != 2:
#         print ("Ungültige Zeit")
#         sys.exit(1)
#     print ("Uhrzeit Ende (" + now + ")" )
#     etime =  sys.stdin.readline()[:-1]
#     if etime != "" and len(etime.split(":")) != 2:
#         print ("Ungültige Zeit")
#         sys.exit(1)
#     print ("Titel")
#     title =  sys.stdin.readline()[:-1]
#     print ("Untertitel")
#     subtitle =  sys.stdin.readline()[:-1]
#     print ("Text")
#     text = ""
#     for line in sys.stdin.readlines():
#         text += line
#     print ("URL")
#     locURL =  sys.stdin.readline()[:-1]
#     print ("Ort")
#     place =  sys.stdin.readline()[:-1]
#     print ("Author")
#     author =  sys.stdin.readline()[:-1]

#     url = "/" + Date.split("T")[0].replace("-","/") + "/" + Time.replace(":","/") + "/"
    
    
#     cont = {"date" : Date, "time" : Time, "etime" : etime, "title" : title, "subtitle" : subtitle, "text" : text, "url" : url, "place" : place, "author" : author, "locURL" : locURL, }
#     curr_events = {}
#     curr_events[str(Date) + "_" + Time +  "_" + place.replace(" ","").replace(",","")] = cont
#     return curr_events

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")


def normalize_date(Date):
    global month
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
                date_fields[1] =  "{:02d}".format(months.index(date_fields[1])+1)
            except:
                print ("Ungültiges Datum")
                sys.exit(1)
            ret = date_fields[2] + "-" + date_fields[1] + "-" + date_fields[0]
        else:
            print ("Ungültiges Datum")
    return ret

def text2ascii(text):
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


def pretty_date(date,time):
    date_parts = date.split("-")
    time_parts = time.split(":")
    return date_parts[2] + ". " + months[int(date_parts[1])-1] + " " + date_parts[0] + ", " + time_parts[0] + ":" + time_parts[1]

           
def dict2eventMD(ev_dict, publish_delta):

    for item in ev_dict:
        dlist = str(ev_dict[item]['date']).split("-")
        tlist = str(ev_dict[item]['time']).split(":")
        outFN = outDir + "/" + dlist[0] + "-" + dlist[1] + "-" + dlist[2] + "_" + tlist[0] + ":" + tlist[1] + "_" + text2ascii(str(ev_dict[item]['title'])).replace(" ","_") + ".md"
        outFF = open(outFN, "w")
        outstr = "---\n" + \
        "layout:        events\n" + \
        "title:         \"" + str(ev_dict[item]['title']) + "\"\n" + \
        "subtitle:      \"" + str(ev_dict[item]['subtitle']) + "\"\n" + \
        "date:          " + str(ev_dict[item]['date']) + "T" +  str(ev_dict[item]['time']) + "\n" + \
        "etime:         " + str(ev_dict[item]['date']) + "T" +  str(ev_dict[item]['etime']) + "\n" + \
        "publishdate:   " + get_publish_date(ev_dict[item]['date'],publish_delta) + "T00:00:00+01:00\n" + \
        "author:        \"" + str(ev_dict[item]['author']) + "\"\n" + \
        "place:         \"" + text2ascii(str(ev_dict[item]['place'])) + "\"\n" + \
        "URL:           \"/" + dlist[0] + "/" + dlist[1] + "/" + dlist[2] + "/" + tlist[0] + "/" + tlist[1] + "/" + text2ascii(str(ev_dict[item]['title'])).replace(" ","_").lower() + "\"\n" + \
        "locURL:        \"" + str(ev_dict[item]['locURL']) + "\"\n" + \
        "image:         \"" + str(ev_dict[item]['image']) + "\"\n" + \
        "---\n" + \
        "\n**Veranstaltung: " + pretty_date(ev_dict[item]['date'],ev_dict[item]['time']) + " Uhr**\n" \
        "\n" + str(ev_dict[item]['title']) + "\n===========\n"
        if str(ev_dict[item]['subtitle']) != "":
            outstr += "\n" + str(ev_dict[item]['subtitle']) + "\n-----------\n"
        outstr += "\n" + str(ev_dict[item]['text']) + "\n" + \
        "\nMehr Informationen auf der [Webseite des Veranstalters](" + str(ev_dict[item]['locURL']) + ")\n"
        print (outstr)
        outFF.write(outstr)
        outFF.close()
        print( "Written to: " + outFN)



##########################
if __name__ == '__main__':
    if len(sys.argv) == 1:
        evt = get_event()
    else:
        evt = get_event(file=sys.argv[1])
        
    outDir = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/content/event/"
    publish_delta = 100
    dict2eventMD(evt, publish_delta)
    
