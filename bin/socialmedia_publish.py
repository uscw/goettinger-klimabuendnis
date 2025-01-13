#!/usr/bin/python3
import os
import sys
import json
from datetime import date, datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from mastodon import Mastodon

tdelta = 3 # timedelta to next event to post 
baseFDIR = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/"
#baseFDIR = "/home/gkb_user/goettinger-klimabuendnis/"
eventFDIR = baseFDIR + "content/event/"
eventImgFDIR = baseFDIR + "static/img/event/"
baseURL = "https://goettinger-klimabuendnis.de/"
eventURL = baseURL + "event/"
cred_fn = "/tmp/Certs/otherCredentials/mastodon_uScw.json"

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
                self.content_lines[k] = line.replace("Kalenderdatei:","").replace("[","").replace("]","").replace("(",": "+baseURL).replace(")","").strip() + "\n"
                break
            k += 1
        for line in self.content_lines[:k]: # Title
            self.post_title += line
        for line in self.content_lines[k:]: # Content incl. ics
            self.post_content += line
        for line in self.content_lines:     # images
            if line.startswith("!["):
                img_line = line.split("(")[1][:-1]
                limit = img_line.rfind("/") + 1
                img_dir = img_line[:limit]
                img_file = img_line[limit:-1]
                self.img_lines.append([img_file, img_dir])
        print ("#### Title",self.post_title,"####")
        # print ("####",self.post_content,"####")
        self.post_content = self.post_content[:self.char_limit-len(self.post_title)]
        limit = self.post_content.rfind(". ")
        self.post_content = self.post_content[:limit+1]      
        print ("#### Content",self.post_content,"####")
        url_ref = baseURL + self.rel_url
        self.post_content += ' ... mehr: ' + url_ref
        return self.post_title, self.post_content, self.img_lines

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
        self.m = Mastodon(access_token=self.token, api_base_url="https://mastodon.social")
        return

    def send_post(self):

        self.title, self.content, self.img_lines = self.prepare_post()
        if len(self.img_lines) == 0:
            out = self.m.toot(self.title + self.content)
        else:
            out = self.send_post_with_image(self.title, self.content, ImgFDIR=self.img_lines[0][1], img_file=self.img_lines[0][0])
        return out

    def send_post_with_image(self, title, content, ImgFDIR=None, img_file=None):
        # for muliple images see: https://buerviper.github.io/blog/2024/writing-a-mastodon-bot-in-python/
        if img_file != None:
            if ImgFDIR == None:
                ImgFDIR = eventImgFDIR 
            os.chdir(ImgFDIR)
            # changes the working directory to /images. If you don't want that, simply skip this and store your python script in the same folder as the images.
            suffix = img_file[img_file.rfind(".")+1:]
            if suffix.lower() in ["jpg", "jpeg"]:
                mtype = "image/jpg"
            elif  suffix.lower() in ["png"]:
                mtype = "image/png"
            else:
                mtype = "image/" + suffix
            self.image = self.m.media_post(img_file, mime_type = mtype, description = content )
            # this is the only required argument. you can either give the filename directly or use the "media_file" argument.
            # this indicates the filetype. only necessarily needed if you did not use "media_type", otherwise the program will guess the correct file type
            # adds alt text. you should definitely consider this!

        # Write a post with an image
        self.m.status_post(title + content, media_ids=self.image["id"] )
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
        try:
            cred_file = open(cred_fn, "r")
            fjson = json.loads(cred_file.read())
            tk = fjson["token"]
        except:
            print ("Access Token for Mastodon not found at " + cred_fn)
            # sys.exit(1)
        return tk
        

class bluesky_post(SM_post):
    def __init__(self, content_lines, fm_lines):
        self.char_limit = 400
        self.content_lines = content_lines
        self.fm_lines = fm_lines
        self.rel_url = self.get_rel_url()
        return
        

def main():
    dt_now = datetime.strftime(datetime.now()+timedelta(days=tdelta),"%Y-%m-%d")
    for file in os.listdir(eventFDIR):
        if file.startswith(dt_now):
            ff = open(eventFDIR + file)
            content_lines = ff.readlines()
            Article = article
            frontmatter, content = Article.content_separation(content_lines)
            print (frontmatter)
            print (content)
            
            Mastodon_Post = mastodon_post(content,frontmatter)
            # post = Mastodon_Post.prepare_post()
            # print (post)
            out = Mastodon_Post.send_post()
            print(out)
    
##########################
if __name__ == '__main__':
    main()
