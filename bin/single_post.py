#!/usr/bin/python

import sys
from datetime import date, datetime, timedelta

PostDir="/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/content/event/"

def get_post():
    today = datetime.now().strftime('%Y-%m-%d')
    print ("Datum (" + today + ")")
    Date = sys.stdin.readline()[:-1]
    if Date == "":
        Date = today
    now = datetime.now().strftime('%H:%M')
    print ("Uhrzeit (" + now + ")" )
    Time =  sys.stdin.readline()[:-1]
    if Time == "":
        Time = now
    print ("Titel")
    title =  sys.stdin.readline()[:-1]
    print ("Untertitel")
    subtitle =  sys.stdin.readline()[:-1]
    print ("Text")
    text = ""
    for line in sys.stdin.readlines():
        text += line
    print ("URL f. weitere Informationen")
    url =  sys.stdin.readline()[:-1]
    print ("Author")
    author =  sys.stdin.readline()[:-1]
    print ("Draft [FALSE|true]")
    draft =  sys.stdin.readline()[:-1]
    if draft == "" or draft.lower() not in  ["false"|"true"]:
        draft = "false"
    else:
         draft = draft.lower()
    
    
    cont = {"date" : Date, "time" : Time, "title" : title, "subtitle" : subtitle, "text" : text, "url4infos" : url, "author" : author, "draft" : draft}
    curr_posts = {}
    curr_posts[str(Date) + "-" + title.replace(" ","_").replace(",","").replace(":","").replace(";","").replace("[","").replace("]","")  +  "-" + author.replace(" ","")] = cont
    return curr_posts

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")


##########################
if __name__ == '__main__':
    pst = get_post()
    print (pst)

    for post in pst:
        Pst = pst[post]

    try:
        LocURL = locURL[Evt["organizer"]][0]
        LocIcon = locURL[Evt["organizer"]][1]
    except:
        LocURL = ""
        LocIcon = "goest-icon.png"

    fo = open(PostDir + post + ".md", "w")
    fo.write("---"+ "\n")
    fo.write("layout:        events"+ "\n")
    fo.write("title:         \"" + Pst["title"] + "\""+ "\n")
    fo.write("subtitle:      \"" + Pst["subtitle"] + "\""+ "\n")
    fo.write("date:          " + Pst["date"] + "T" + Pst["time"] + ":00+01:00"+ "\n")
    fo.write("publishdate:   " + get_publish_date(Pst["date"],0) + "T00:00:00+01:00"+ "\n")
    fo.write("author:        \"" + Pst["author"] + "\""+ "\n")
    fo.write("draft:        \"" + Pst["draft"] + "\""+ "\n")
    fo.write("---"+ "\n")
    fo.write(""+ "\n")
    fo.write(Pst["title"]+ "\n")
    fo.write("==========="+ "\n")
    fo.write(""+ "\n")
    fo.write(Pst["subtitle"]+ "\n")
    fo.write("-----------"+ "\n")
    fo.write(""+ "\n")
    fo.write(Pst["text"])
    fo.write(""+ "\n")
    if Pst["url4infos"] != "":
        fo.write("[Weitere Informationen...](" + Pst["url4infos"] + ")"+ "\n")
    fo.close()
