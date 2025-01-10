#!/usr/bin/python3
import os
import sys
from datetime import date, datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from mastodon import Mastodon

baseFDIR = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/"
eventFDIR = baseFDIR + "content/event/"
eventImgFDIR = baseFDIR + "static/img/event/"
baseURL = "https://goettinger-klimabuendnis.de/"
eventURL = baseURL + "event/"

class article():
    def __init__(self):
        return
    
    def content_separation(content_lines):
        fm_delims = []
        k = 0
        for line in content_lines:
            if line == "---\n":
                fm_delims.append(k)
            k += 1
        return content_lines[fm_delims[0]:fm_delims[1]+1],content_lines[fm_delims[1]+1:]

class SM_post():
    def __init__(self, content_lines, fm_lines):
        self.char_limit = 1000
        self.content_lines = content_lines
        self.fm_lines = fm_lines
        self.rel_url = self.get_rel_url()
        return

    def prepare_post(self):
        self.post_title = ""
        self.post_content = ""
        self.img_lines = []
        post_content_lines = False
        k = 0
        for line in self.content_lines:
            if line.startswith("Kalenderdatei:"):
                self.content_lines[k] = line.replace("Kalenderdatei:","").replace("[","").replace("]","").replace("(",": "+baseURL).replace(")","").strip()
                break
            k += 1
        for line in self.content_lines[k:]:
            self.post_title += line
        for line in self.content_lines[k:]:
            self.post_content += line
            if line.startswith("!["):
                self.img_lines.append(line)
        print ("#### Title",self.post_title,"####")
        # print ("####",self.post_content,"####")
        self.post_content = self.post_content[:self.char_limit-len(self.post_title)]
        limit = self.post_content.rfind(". ")
        self.post_content = self.post_content[:limit+1]      
        print ("#### Content",self.post_content,"####")
        url_ref = baseURL + self.rel_url
        self.post_content += ' ... mehr: ' + url_ref
        return self.post_title, self.post_content 

    def get_rel_url(self):
        for line in self.fm_lines:
           if line.strip().startswith("URL:"):
               return line[5:].strip().replace('"','')
           


class mastodon_post(SM_post):
    def __init__(self, content_lines, fm_lines):
        self.char_limit = 500
        self.content_lines = content_lines
        self.fm_lines = fm_lines
        self.rel_url = self.get_rel_url()
        self.token = self.get_token()
        return

    def send_post(self):
        m = Mastodon(access_token=self.token, api_base_url="https://mastodon.social")
        self.title, self.content = self.prepare_post()
        if len(self.img_line) == 0:
            out = m.toot(post)
        else:
            out = self.send_post_with_image(self.title, self.content, caption, ImgFDIR=None, img_file=None):
        return out

    def send_post_with_image(self, title, caption, ImgFDIR=None, img_file=None):
        m = Mastodon(access_token=self.token, api_base_url="https://mastodon.social")
        if img_file != None:
            if ImgFDIR == None:
                ImgFDIR = eventImgFDIR 
            os.chdir(ImgFDIR)
            # changes the working directory to /images. If you don't want that, simply skip this and store your python script in the same folder as the images.
            suffix = img_file[img_file.rfind("."):]
            if suffix.lower() in ["jpg", "jpeg"]:
                mtype = "image/jpg"
            elif  suffix.lower() in ["png"]:
                mtype = "image/png"
            else:
                mtype = None
            self.image = m.media_post(img_file, mime_type = mtype, description = None )
            # this is the only required argument. you can either give the filename directly or use the "media_file" argument.
            # this indicates the filetype. only necessarily needed if you did not use "media_type", otherwise the program will guess the correct file type
            # adds alt text. you should definitely consider this!

        # Write a "Hello World!" post with an image
        mastodon.status_post(caption, media_ids=self.image["id"] )
        # this is the text associated with the message
        # as said earlier, the media_post function uploads the image with an id as a dictionary. this calls the correct photo
        return self.image

    def get_img_dir(self, img_line):
        img_ptr = img_line.split("(")[1][:-1]
        last_slash = img_ptr.rfind("/")
        img_prefix = img_ptr[:last_slash]
        img_file = img_ptr[last_slash:]
        return img_prefix, img_file
    
    def delete_post(self,id):
        return

    def get_token(self):
        tk = "pth6ujxYWEQbjYX3USVtrZ0jgDnL3grooFTxiRnemAs"
        return tk
        

class bluesky_post(SM_post):
    def __init__(self, content_lines, fm_lines):
        self.char_limit = 400
        self.content_lines = content_lines
        self.fm_lines = fm_lines
        self.rel_url = self.get_rel_url()
        return
        

def main():
    # dt_now = datetime.strftime(datetime.now()+timedelta(days=3), "%Y-%m-%d-%H%M")
    dt_now = datetime.strftime(datetime.now()+timedelta(days=3), "%Y-%m-%d")
    for file in os.listdir(eventFDIR):
        if file.startswith(dt_now):
            ff = open(eventFDIR + file)
            content_lines = ff.readlines()
            Article = article
            frontmatter, content = Article.content_separation(content_lines)
            print (frontmatter)
            print (content)
            
            Mastodon_Post = mastodon_post(content,frontmatter)
            post = Mastodon_Post.prepare_post()
            print (post)
            out = Mastodon_Post.send_post()
            print(out)
    
##########################
if __name__ == '__main__':
    main()
