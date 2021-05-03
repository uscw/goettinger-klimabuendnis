import sys
import events_p3_dt as dt # Deutsches Theater
import events_p3_jt as jt # Junges Theater
import events_p3_lm as lm # Lumiere
import events_p3_lz as lz # Literarisches Zentrum
import events_p3_to as to # Theater im OP
# import events_p3_ff as ff # Filmfest Goettingen
import events_p3_ex as ex # Exil


from datetime import date, datetime, timedelta
import traceback

def get_publish_date(date_str, publish_delta):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    publish_date = date - timedelta(days=publish_delta)
    return publish_date.strftime("%Y-%m-%d")

def dict2eventMD(ev_dict, publish_delta):

    for item in ev_dict:
        outFN = outDir + item + ".md"
        outFF = open(outFN, "w")
        dlist = str(ev_dict[item]['date']).split("-")
        tlist = str(ev_dict[item]['time']).split(":")
        outFF.write("---\n"
            "layout:        events\n" \
    	"title:         \"" + str(ev_dict[item]['title']) + "\"\n" \
    	"subtitle:      \"" + str(ev_dict[item]['subtitle']) + "\"\n" \
    	"date:          " + str(ev_dict[item]['date']) + "T" +  str(ev_dict[item]['time']) + ":00+01:00\n" \
    	"publishdate:   " + get_publish_date(ev_dict[item]['date'],publish_delta) + "T00:00:00+01:00\n" \
    	"author:        \"" + str(ev_dict[item]['place']) + "\"\n" \
    	"place:         \"" + str(ev_dict[item]['place']) + "\"\n" \
        "URL:           \"/" + dlist[0] + "/" + dlist[1] + "/" + dlist[2] + "/" + tlist[0] + "/" + tlist[1] + "/" + str(ev_dict[item]['place']).lower().replace(" ","") + "\"\n" \
    	"icon:         \"" + str(ev_dict[item]['locICON']) + "\"\n" \
    	"image:         \"" + str(ev_dict[item]['locIMG']) + "\"\n" \
    	"locURL:         \"" + str(ev_dict[item]['locURL']) + "\"\n" \
    	"---\n")
        outFF.write("\n" + str(ev_dict[item]['title']) + "\n===========\n")
        outFF.write("\n" + str(ev_dict[item]['subtitle']) + "\n-----------\n")
        outFF.write("\n" + str(ev_dict[item]['text']) + "\n")
        outFF.write("\nMehr Informationen auf der [Webseite des Veranstalters](" + str(ev_dict[item]['url']) + ")\n")
    
        outFF.close()
        print( "Written to: " + outFN)

##########################
if __name__ == '__main__':

    today = date.today()
    Today = today.strftime("%Y-%m-%d")
    today30 = today + timedelta(30)
    Today30 = today30.strftime("%Y-%m-%d")
    publish_delta = 10
    outDirBase = "/home/uschwar1/ownCloud/AC/html/hugo/goest/content/event/"
    if (len(sys.argv) == 2): 
        outDirBase = sys.argv[1]
        if outDirBase[-1] != "/":
            boutDirBase += "/"
        
    try:
        events = {}
        JT = jt.events()
        events.update(JT.current_events)
        outDir = outDirBase + "JungesTheater/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Junges Theater\n" + traceback.format_exc())


    try:
        events = {}
        DT = dt.events()
        events.update(DT.current_events)
        outDir = outDirBase + "DeutschesTheater/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Deutsches Theater\n" + traceback.format_exc())

    try:
        events = {}
        LM = lm.events()
        events.update(LM.current_events)
        outDir = outDirBase + "Lumiere/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Lumiere\n" + traceback.format_exc())

    try:
        events = {}
        LZ = lz.events()
        events.update(LZ.current_events)
        outDir = outDirBase + "LiterarischesZentrum/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Literarisches Zentrum\n" + traceback.format_exc())

    try:
        events = {}
        TO = to.events()
        events.update(TO.current_events)
        outDir = outDirBase + "TheaterImOP/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Theater Im OP\n" + traceback.format_exc())

    try:
        events = {}
        EX = ex.events()
        events.update(EX.current_events)
        outDir = outDirBase + "Exil/"
        dict2eventMD(events, publish_delta)
    except:
        print ("Error: Exil\n" + traceback.format_exc())
    
