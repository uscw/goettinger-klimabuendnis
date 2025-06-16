from PIL import Image, ImageDraw, ImageFont, ImageColor
import random


hsize = 500
vsize = 500
random_box = True
fontname = "LiberationSans-Bold.ttf"
fontsize = 28
image_file = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/static/img/banner/2025-06-13-Brennende-Erde.jpg"
output_path = "out.jpg"

class bg_canvas():
    def __init__(self, hsize, vsize, image):
        self.hsize = hsize
        self.vsize = vsize
        self.image = image
        (self.Hsize,self.Vsize)=self.image.size
        if random_box:
            xx = random.randrange(0, self.Hsize - self.hsize)
            yy = random.randrange(0, self.Vsize - self.vsize)
            self.box = (xx,yy,xx+hsize,yy+vsize)
        else: # use the middle of the image as default
            xx = (self.Hsize - self.hsize)/2
            yy = (self.Vsize - self.vsize)/2
            self.box = (xx,yy,hsize,vsize)

    def crop_region(self):
        self.region = self.image.crop(self.box)
        return self.region

    def grey2subregion(self,textheight):
        self.subbox = (xx,yy,hsize,vsize)
        
    def text_in_region(self, text_lines, xOff, yOff, font, fontsize=fontsize, black_offset=5, color="white"):
        ll = ImageColor.getrgb("brown")
        ll = color
        # bright_color = (int(ll[0]*2),int(ll[1]*2),int(ll[2]*2))

        #collist = []
        #for i in range(len(color)):
        #    collist.append(int(color[i]*0.5))
        #print(collist)
        #bright_color = (collist[0],collist[1],collist[2])

        #bright_color = (R,color[1],color[2])#int(color[1]*0.5),int(color[2]*0.5))
        self.draw = ImageDraw.Draw(self.region)
        i = 0
        for line in text_lines:
            self.draw.text((xOff + black_offset, yOff + int(1.1 * fontsize*i) + black_offset), line, font=font, fill="black")
            i += 1
        i = 0
        for line in text_lines:
            self.draw.text((xOff, yOff + int(1.1 * fontsize*i)), line, font=font, fill=color)
            i += 1

    def dominant_color_in_region(self,region,brighter=False):
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
        if brighter:            
            return (min(int(dom_cols[0][0][0]*1.5),255),min(int(dom_cols[0][0][1]*1.5),255),min(int(dom_cols[0][0][2]*1.5),255))
        else:
            return (dom_cols[0][0][0],dom_cols[0][0][1],dom_cols[0][0][2])


class text_field():
    def __init__(self,text,fontname=fontname,fontsize=fontsize): # fontsize determined in class Font 
        self.text = text.replace("\n"," ").strip()
        self.fontname = fontname
        self.fontsize = fontsize
        self.font = ImageFont.truetype(self.fontname, self.fontsize)
        return

    def break_text(self, max_width, max_height):
        txt = self.text
        text_lines = []
        break_point = len(txt)
        rlast_break_point = break_point
        llast_break_point = break_point
        letter_size = None    
        text_size = len(txt)
        # We share the subset to remember the last finest guess over 
        # the text breakpoint and make it faster
        text_too_long = False
        while text_size > 0:
            # Let's find the appropriate subset size
            while True:
                x,y,width,height = self.font.getbbox(txt[:break_point])
                letter_size = width / break_point
    
                # min/max(..., break_point +/- 1) are to avoid looping infinitely over a wrong value
                if width < max_width - letter_size and text_size >= break_point: # Too short
                    rlast_break_point = break_point
                    break_point = max(int(max_width * break_point / width), break_point + 1)
                elif width > max_width: # Too large
                    llast_break_point = break_point
                    break_point = min(int(max_width * break_point / width), break_point - 1)
                else: # Break_Point fits, we exit
                    break
                if rlast_break_point == break_point or llast_break_point == break_point:
                    break
            print("a",break_point)
            blank_break_point = txt[:break_point].rfind(" ")
            if blank_break_point > 0:
                break_point = blank_break_point
                # print("b",break_point)
            text_lines.append(txt[:break_point])
            txt = txt[break_point+1:]   
            text_size = len(txt)
            if len(text_lines) * int(1.1 * self.fontsize) > max_height:
                text_too_long = True
                break
        if not text_too_long:
            text_lines[-2] += " " +text_lines[-1]
            text_lines = text_lines[:-1]
        self.text_lines = text_lines
        return text_lines


if __name__ == "__main__":
#    text("/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/static/img/banner/2024-08-21-Zusammen-fuer-unsere-Zukunft.jpg", "out.jpg")
    image = Image.open(image_file)
    BG = bg_canvas(hsize, vsize, image)
    region = BG.crop_region()
    text = "Das kann man nicht ohne weiteres wissen (und das ist in der Handle-Welt so gewollt). Metadaten von 10013 (das ist der Prefix in dem genannten Handle) deuten auf AWI (Bremerhaven). Wie kann ich solche Dinge selbst rausbekommen?"
    #, font1=font, fontsize1=fontsize, font2=font, fontsize2=fontsize):
    text = text[:40]
    # fonts in /usr/share/fonts/truetype
    fontname1 = "LiberationSans-Bold.ttf"
    fontsize1 = 42
    Title = text_field(text,fontname=fontname1,fontsize=fontsize1)
    xoffset = 15
    textbox_width = 500 - xoffset
    max_textbox_height = 300
    textlines = Title.break_text(textbox_width, max_textbox_height)
    textbox_height = int(fontsize1 * 1.1 * len(textlines)) + xoffset
    yoffset = 20 + (max_textbox_height - min(max_textbox_height,textbox_height))
    textbox = (xoffset, yoffset, textbox_width, yoffset + textbox_height)
    subregion = region.crop(textbox)
    subregion_grey = subregion.convert('L')
    region.paste(subregion_grey,(textbox[0], textbox[1]))
    dom_col = BG.dominant_color_in_region(region,brighter=True)
    BG.text_in_region(textlines, textbox[0], textbox[1], Title.font, fontsize=Title.fontsize, color=dom_col)

    wann_tag = "Sa. 14.06.2025"
    wann_zeit = "19:00 Uhr"
    wo1 = "Kerstlingeröder Feld"
    wo2 = "Göttingen"
    fontname2 = "Courier-Bold.ttf"
    fontsize2 = 28
    Wann_Wo =  text_field(text,fontname=fontname2,fontsize=fontsize2)
    Wann_Wo.text_lines = [
        "Wann: " + wann_tag,
        "      " + wann_zeit,
        "Wo:   " + wo1,
        "      " + wo2
    ]
    BG.text_in_region(Wann_Wo.text_lines, 15, 370, Wann_Wo.font, fontsize=Wann_Wo.fontsize, black_offset=3)
    region.show()
    # region.save(output_path)
    
