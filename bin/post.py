#!/usr/bin/python

import sys
import os
from datetime import date, datetime, timedelta

PostDir="/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/content/post/"
homeDir = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis"
banner_dir = "/img/banner"
default_banner = "/img/banner/2021-12-17_Kundgebung_Rathaus_Goettingen_klimaneutral_2030.jpg"

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

    print ("Banner-Bild:")
    for file in os.listdir(homeDir + "/static" + banner_dir):
        print(file)
    Image = sys.stdin.readline()[:-1]
    if Image == "":
        Image = default_banner
    else:
        Image = banner_dir + "/" + Image
    print ("Author")
    author =  sys.stdin.readline()[:-1]
    print ("Show Table of Content [FALSE|true]")
    showtoc =  sys.stdin.readline()[:-1].lower()
    if showtoc == "" or showtoc not in  ["false","true"]:
        showtoc = "false"
    print ("Draft [FALSE|true]")
    draft =  sys.stdin.readline()[:-1].lower()
    if draft == "" or draft not in  ["false","true"]:
        draft = "false"
     
    
    cont = {"date" : Date, "time" : Time, "title" : title, "subtitle" : subtitle, "text" : text, "url4infos" : url, "image" : Image, "author" : author, "showtoc" : showtoc, "draft" : draft}
    curr_posts = {}
    curr_posts[(str(Date) + "_" + Time + "-" + title  +  "-" + author).replace(" ","_").replace(",","").replace(":","").replace(";","").replace("[","").replace("]","").replace("!","").replace("/","")] = cont
    return curr_posts

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")


##########################
if __name__ == '__main__':
    publish_delta = 100

    pst = get_post()

    for post in pst: # should be only one
        print (post)
        print (pst)
        Pst = pst[post]

    try:
        LocURL = locURL[Evt["organizer"]][0]
        LocIcon = locURL[Evt["organizer"]][1]
    except:
        LocURL = ""
        LocIcon = ""

    fo = open(PostDir + post + ".md", "w")
    
    fo.write("---"+ "\n")
    fo.write("layout:        posts"+ "\n")
    fo.write("title:         \"" + Pst["title"] + "\""+ "\n")
    fo.write("subtitle:      \"" + Pst["subtitle"] + "\""+ "\n")
    fo.write("date:          " + Pst["date"] + "T" + Pst["time"] + ":00+01:00"+ "\n")
    fo.write("publishdate:   " + get_publish_date(Pst["date"],publish_delta) + "T00:00:00+01:00"+ "\n")
    if Pst["image"] != "":
        fo.write("image:         \"" + Pst["image"] + "\""+ "\n")
    fo.write("author:        \"" + Pst["author"] + "\""+ "\n")
    fo.write("showtoc:      " + Pst["showtoc"] + "\n")
    fo.write("draft:        " + Pst["draft"] + "\n")
    fo.write("---"+ "\n")
    fo.write(""+ "\n")
    # fo.write(Pst["title"]+ "\n")
    # fo.write("==========="+ "\n")
    # fo.write(""+ "\n")
    # fo.write(Pst["subtitle"]+ "\n")
    # fo.write("-----------"+ "\n")
    # fo.write(""+ "\n")
    fo.write(Pst["text"])
    fo.write(""+ "\n")
    if Pst["url4infos"] != "":
        fo.write("[Weitere Informationen...](" + Pst["url4infos"] + ")"+ "\n")
    fo.close()
    print ("Written to file:\n" + PostDir + post + ".md")
