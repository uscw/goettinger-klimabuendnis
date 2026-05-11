
PIC = "https://climatejustice.global/system/media_attachments/files/116/517/209/550/114/982/original/07311298f091e4a0.jpg"



from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class img():
    def __init__(self, url):
        response = requests.get(PIC)
        self.fontname = "LiberationSans-Bold.ttf"
        self.fontsize = 52
        self.font = ImageFont.truetype(self.fontname, self.fontsize)
        self.image = Image.open(BytesIO(response.content))
        (self.Hsize,self.Vsize) = self.image.size
        self.box = (0.,0.,self.Hsize,self.Vsize)
 
    def text_shadow_in_region(self, text_lines, color="red"):
        # lower_vertical_textbox_offset = int(self.Vsize * 1/5) # text_height = vsize * 20%
        #self.region = self.set_text_region()
        black_offset = int(self.fontsize/10)
        self.draw = ImageDraw.Draw(self.image)
        xOff = self.box[0] + 10
        yOff = self.box[3] * 0.2
        i = 0
        for line in text_lines:
            self.draw.text((xOff + black_offset, yOff + int(1.1 * self.fontsize*i) + black_offset), line, font=self.font, fill="black")
            i += 1
        i = 0
        for line in text_lines:
            self.draw.text((xOff, yOff + int(1.1 * self.fontsize*i)), line, font=self.font, fill=color)
            i += 1

Img = img(PIC)

Img.text_shadow_in_region(["!!! fällt leider aus !!!"])
print (Img.Hsize,Img.Vsize)
#print (Img.region)
Img.image.show()
#Img.region.show()

