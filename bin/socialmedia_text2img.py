from PIL import Image, ImageDraw, ImageFont, ImageColor
import sys
import random
import locale
from datetime import datetime

hsize = 500
vsize = 700
random_box = True
fontname = "LiberationSans-Bold.ttf"
fontsize = 28
#image_file = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/static/img/banner/2025-06-13-Brennende-Erde.jpg"
output_path = "/tmp/out.jpg"

GoeKBhome = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/"
eventFDIR = GoeKBhome + "content/event/"
GoeKBwebHome = "https://goettinger-klimabuendnis.de" 

class bg_canvas():
    def __init__(self, hsize, vsize, verbosity=1):
        self.hsize = hsize
        self.vsize = vsize
        self.fhsize = hsize*0.9
        self.fvsize = vsize*0.9
        
        self.verbosity = verbosity
        
    def get_image(self,image_file):
        self.image = image_file
        (self.Hsize,self.Vsize)=self.image.size
        
    def get_region_in_image(self):
        if self.Vsize < self.vsize:
            self.image = self.image.resize((int(self.hsize*self.vsize/self.Vsize)+1,self.vsize+1))
            (self.Hsize,self.Vsize)=self.image.size
        if self.Hsize < self.hsize:
            self.image = self.image.resize((self.hsize+1,int(self.vsize*self.hsize/self.Hsize)+1))
            (self.Hsize,self.Vsize)=self.image.size
        if random_box:
            xx = random.randrange(0, self.Hsize - self.hsize)
            yy = random.randrange(0, self.Vsize - self.vsize)
            # print((0, self.Hsize - self.hsize))
            self.box = (xx,yy,xx+hsize,yy+vsize)
            # print(self.box)
        else: # use the middle of the image as default
            xx = (self.Hsize - self.hsize)/2
            yy = (self.Vsize - self.vsize)/2
            self.box = (xx,yy,xx+hsize,yy+vsize)
        self.region = self.image.crop(self.box)

    def grey2subregion(self,textheight):
        return
        self.subbox = (xx,yy,hsize,vsize)
        
    def text_shadow_in_region(self, text_lines, xOff, yOff, font, fontsize=fontsize, color="white"):
        black_offset = int(fontsize/10)
        self.draw = ImageDraw.Draw(self.region)
        i = 0
        for line in text_lines:
            self.draw.text((xOff + black_offset, yOff + int(1.1 * fontsize*i) + black_offset), line, font=font, fill="black")
            i += 1
        i = 0
        for line in text_lines:
            self.draw.text((xOff, yOff + int(1.1 * fontsize*i)), line, font=font, fill=color)
            i += 1

    def color_sum(color):
        sumc = 0
        for i in range(len(color)):
            if new_col[i] > maxc:
                maxc = i
            sumc += new_col[i]
        
            
    def dominant_color_in_region(self,region,brighter=False):
        color_sum_threshold = 150
        color_brightener = 2.0
        dictc={}
        for i in range( region.width ):
            for j in range( region.height ) :
                h = region.getpixel( ( i,j ) )
                if h in dictc:
                    dictc[h] = dictc[h] + 1
                else:
                    dictc[h]=1  
        #now sort it by values rather than keys descending
        dom_cols = sorted(dictc.items(), key=lambda x: x[1], reverse=True)
        new_col = []
        bright = False
        maxc = 0
        sumc = 0
        while sumc < color_sum_threshold:
            for i in range(len(dom_cols[0][0])):
                new_col.append(dom_cols[0][0][i])
                if new_col[i] > maxc:
                    maxc = i
                sumc += new_col[i]
                if sumc < color_sum_threshold:  # then complement all non-max-colors 
                    for i in range(len(new_col)):
                        if i != maxc:
                            new_col[i] = 255 - new_col[i]  
        compl_col = (255-new_col[0],255-new_col[1],255-new_col[2])
        if brighter:
            new_col = (min(int(new_col[0]*color_brightener),255),min(int(new_col[1]*color_brightener),255),min(int(new_col[2]*color_brightener),255))
            compl_col = (min(int(compl_col[0]*color_brightener),255),min(int(compl_col[1]*color_brightener),255),min(int(compl_col[2]*color_brightener),255))
        return  new_col, compl_col

    def buildPic(self,title,subtitle,wann,wo,wer,url=None):
        # wann in Format: '2025-06-13T15:30:00+02:00'
        # fonts in /usr/share/fonts/truetype
        #
        # requires:
        # self.region
        fontname1 = "LiberationSans-Bold.ttf"
        fontsize1 = 42
        fontname2 = "LiberationSans-Bold.ttf"
        fontsize2 = 18
        fontname3 = "Courier-Bold.ttf"
        fontsize3 = 28

        # general parameters depending only 
        self.xhoffset = int(self.hsize * 3/100)          # xhoffset = 3 %
        self.textbox_width = self.hsize - 2*self.xhoffset  # text_width = hsize - 6 %
        self.addBoxHeight = int(self.hsize * 8/100)
        self.upperTextBound = int(self.hsize * 4/100)
        self.leftTextBound = int(self.hsize * 1/100)

        lower_vertical_textbox_offset = int(self.vsize * 3/5) # text_height = vsize * 60%
        self.max_textbox_height = lower_vertical_textbox_offset 
        Title = text_field(text=title,fontname=fontname1,fontsize=fontsize1, max_width=self.textbox_width, max_height=self.max_textbox_height)
        textlines = Title.break_text()
        textbox_region = Title.get_text_region(self.xhoffset, self.upperTextBound, self.addBoxHeight)
        tb_region_height = textbox_region[3] - textbox_region[1] - 2*self.addBoxHeight

        # extract colers  under title lines and build grey subregion there
        subregion = self.region.crop(textbox_region)
        dom_col, compl_col = self.dominant_color_in_region(subregion,brighter=True)
        subregion_grey = subregion.convert('L')
        self.region.paste(subregion_grey,(textbox_region[0], textbox_region[1]))

        # place title lines at the top in grey subregion
        text_x = textbox_region[0]+self.leftTextBound
        text_y = textbox_region[1]+self.addBoxHeight
        self.text_shadow_in_region(textlines, text_x, text_y, Title.font, fontsize=Title.fontsize, color=dom_col)
        ###
        
        #self.place_text_in_subregion(title,fontname,fontsize,textbox_region,tb_region_height,dom_col)
        
        # place subtitle lines at the bottom in grey subregion
        ###
        self.max_textbox_height = int(self.vsize * 4/100) # text_height = vsize * 4 %
        Subtitle = text_field(text=subtitle,fontname=fontname2,fontsize=fontsize2, max_width=self.textbox_width, max_height=self.max_textbox_height)
        textlines = Subtitle.break_text()


        text_x = textbox_region[0] + self.leftTextBound
        text_y = textbox_region[1] + tb_region_height + self.addBoxHeight - 10
        self.text_shadow_in_region(textlines, text_x, text_y, Subtitle.font, fontsize=Subtitle.fontsize, color=dom_col)

        # place Wann, Wo, Wer below the grey subregion
        ###
        textbox_height = int(fontsize2 * 1.1 * len(textlines)) + self.xhoffset
        Wann_Wo =  text_field(fontname=fontname3,fontsize=fontsize3)
        textlines = Wann_Wo.get_time_place_lines(wann,wo,wer)
        text_x = self.hsize * 3/100
        text_y = text_y + textbox_height + 30
        self.text_shadow_in_region(textlines, text_x, text_y, Wann_Wo.font, fontsize=fontsize3, color=compl_col)
        if self.verbosity > 0:
            self.region.show()
        # region.save(output_path)
        return self.region

    def place_text_in_subregion(self,text,fontname,fontsize,textbox_region,tb_region_height,dom_col):
        Text = text_field(text=text,fontname=fontname,fontsize=fontsize)
        max_textbox_height = int(self.vsize * 4/100) # text_height = vsize * 4 %
        textlines = Text.break_text(self.textbox_width, self.max_textbox_height)
        # textbox_height = int(fontsize * 1.1 * len(textlines)) + self.xhoffset
        text_x = textbox_region[0]+self.leftTextBound
        text_y = textbox_region[1] + tb_region_height + self.addBoxHeight - 10
        self.text_shadow_in_region(textlines, text_x, text_y, Text.font, fontsize=Text.fontsize, color=dom_col)
        

    def buildPicWithFM(self,frontmatter,output_path):
        # wann in Format: '2025-06-13T15:30:00+02:00'
        # print(frontmatter)
        self.image_file = Image.open(GoeKBhome + "static" + frontmatter["image"])
        self.get_image(self.image_file)
        self.get_region_in_image()
        Title = frontmatter["title"]
        Subtitle = frontmatter["subtitle"]
        wann = frontmatter["date"]
        wo = frontmatter["place"]
        wer = frontmatter["author"]
        url = GoeKBwebHome + frontmatter["URL"]
        SharePic = self.buildPic(Title,Subtitle,wann,wo,wer,url=url)
        SharePic.convert('RGB').save(output_path)

    
class text_field():
    def __init__(self,text="", fontname=fontname, fontsize=fontsize, max_width=0, max_height=0): # fontsize determined in class Font 
        self.text = text.replace("\n"," ").strip()
        self.fontname = fontname
        self.fontsize = fontsize
        self.font = ImageFont.truetype(self.fontname, self.fontsize)
        self.max_width = max_width
        self.max_height = max_height
        return

    def break_text(self):
        self.text_lines = []
        txt = self.text
        break_point = len(txt)
        rlast_break_point = break_point
        llast_break_point = break_point
        letter_size = None    
        text_size = len(txt)
        # We share the subset to remember the last finest guess over 
        # the text breakpoint and make it faster, but this might lead to looping
        text_too_long = False
        while text_size > 0:
            # Let's find the appropriate subset size
            while True:
                x,y,width,height = self.font.getbbox(txt[:break_point])
                letter_size = width / break_point
                # print (width, letter_size, max_width)
                if width < self.max_width - letter_size and text_size >= break_point: # Too short
                    rlast_break_point = break_point
                    break_point = max(int(self.max_width * break_point/ width), break_point + 1)
                    bp = txt[:break_point].rfind(" ")
                    if bp == -1:
                        break_point = len(txt[:break_point]) + 1
                    else:
                        break_point = bp
                elif width > self.max_width: # Too large
                    llast_break_point = break_point
                    break_point = min(int(self.max_width * break_point / width), break_point - 1)
                    bp = txt[:break_point].rfind(" ")
                    if bp == -1:
                        break_point = len(txt[:break_point]) + 1
                    else:
                        break_point = bp
                else: # Break_Point fits, exit now
                    break
                if rlast_break_point == break_point or llast_break_point == break_point:
                    break # if looping starts, also Break_Point fits, exit now
            # print("bp:",break_point,"len",len(txt),"txt",txt[:break_point])
            self.text_lines.append(txt[:break_point])
            txt = txt[break_point+1:] # remove heading blank from next text frame 
            text_size = len(txt)
            if break_point < 0:   
                break
            if len(self.text_lines) * int(1.1 * self.fontsize) > self.max_height:
                text_too_long = True
                break
        try:
            x,y,width,height = self.font.getbbox(self.text_lines[-2] + " " + self.text_lines[-1])
            if width < self.max_width - letter_size:
                self.text_lines[-2] += " " + self.text_lines[-1]
                self.text_lines = self.text_lines[:-1]
        except:
            None
        return self.text_lines

        
    def get_text_region(self, xhoffset, upperTextBound, addBoxHeight):
        textbox_height = int(self.fontsize * 1.1 * len(self.text_lines)) + xhoffset
        yoffset = upperTextBound + (self.max_height - min(self.max_height,textbox_height))
        tb_region_width = self.max_width
        tb_region_height = textbox_height
        textbox_region = (xhoffset, yoffset - addBoxHeight, tb_region_width, yoffset + tb_region_height + addBoxHeight)
        return textbox_region

        
    
    def get_time_place_lines(self,wann,wo,wer=""):
        locale.setlocale(locale.LC_ALL, "de_DE")
        textlines = self.get_dt(wann)
        d = wo[:25].rfind(" ")
        textlines.append("Wo:   " + wo[:d])
        wo = wo[d+1:]
        textlines.append("      " + wo[:25])
        if len(wer) < 30:
            d = len(wer)
        else:
            d = wer[:30].rfind(" ")
        wer = "(" + wer[:d] + ") "
        textlines.append(wer.rjust(29))
        return textlines

    def get_dt(self,wann):
        dt = datetime.strptime(wann,"%Y-%m-%dT%H:%M:%S%f%z")
        #dt = datetime.strptime(wann[:wann.find('+')], "%Y-%m-%dT%H:%M:%S")
        dt1 = "Wann: " + dt.strftime("%A, %-d.%-m.%Y")
        dt2 = "      " + dt.strftime("%H:%M Uhr")
        return [dt1,dt2]


class md_file():
    def __init__(self,filename):
        self.frontmatter = self.get_frontmatter(filename)
        return

    def get_frontmatter(self,filename):
        fm_json = {}
        file = open(filename, encoding="utf-8")
        fm_on = False
        for line in file.readlines():

            if fm_on == True and line[:-1] == "---":
                fm_on = False
            elif line[:-1] == "---":
                fm_on = True
            elif fm_on == False:
                continue
            elif fm_on == True:
                spl = line.find(":")
                key = line[:spl]
                value = line[spl+1:]
                try:
                    fm_json[key.strip()] = eval(value.strip()) # .encode())
                except:
                    try:
                        fm_json[key.strip()] = value.strip()
                    except:
                        print("Warning: wrong frontmatter line " + line)
        return fm_json

##########################
if __name__ == "__main__":

    if len(sys.argv) > 1:
        mdfile = sys.argv[1]
    else:
        print ("usage: " + sys.argv[0] + " event_file.md")
        sys.exit(1)
    MD = md_file(eventFDIR + mdfile)
    BG = bg_canvas(hsize, vsize)
    BG.buildPicWithFM(MD.frontmatter,output_path)
