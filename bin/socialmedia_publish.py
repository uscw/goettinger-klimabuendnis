#!/usr/bin/python3
import os
import sys
import json
from datetime import date, datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from email.mime.text import MIMEText
import smtplib
# import imaplib



# Import the Client class for Mastodon
from mastodon import Mastodon
# Import the Client class for Bluesky from the atproto library
from atproto import Client as blueskyClient
from atproto import client_utils as blueskyClientUtils
# Import the Client class for Instagram
from instagrapi import Client as InstaClient


no_posts = True
post_forced = True
tdelta = -8 # timedelta to next event to post 
baseFDIR = "/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/"
#baseFDIR = "/home/gkb_user/goettinger-klimabuendnis/"
eventFDIR = baseFDIR + "content/event/"
eventImgFDIR = baseFDIR + "static/img/event/"
baseURL = "https://goettinger-klimabuendnis.de/"
eventURL = baseURL + "event/"
cred_fdir = "/tmp/Certs/otherCredentials/"
schoenerleben_receivers = ["ulrich.schwardmann@web.de", "ulrich.schwardmann@web.de"]
out_lg = 200

class article():
    
    def __init__(self,article_lines):
        self.article_lines = article_lines
        self.article_parts = self.get_content_separation()
        # self.article_parts["full_title"] = self.get_full_title()        
        # self.article_parts["frontmatter"] = frontmatter
        # self.article_parts["content"] = content
        # self.article_parts["article_separator"] = fm_separator       
        self.article_parts["img_lines"] = self.get_img_lines()
        # self.article_parts["title"] = self.get_title()
        # self.article_parts["subtitle"] = self.get_subtitle()
        # self.article_parts["event_line"] = self.get_event_line()
        # self.article_parts[""] = self.get_()
        # self.article_parts[""] = self.get_()
        self.title_lines = self.get_title_lines()
        # print ("\n****" + "****\n")
        # for item in self.article_parts:
        #     print ("\n****" + item + "****\n" + str(self.article_parts[item]))
        # print ("\n****" + "****\n")
        return
    
    def get_content_separation(self):
        self.article_parts = {}
        fm_delims = []
        k = 0
        l = 0
        frontmatter = {}
        content = ""
        is_frontmatter = None
        lastline = ""
        for line in self.article_lines:
            if line == "---\n":
                if is_frontmatter == None:
                    is_frontmatter = True
                else:
                    is_frontmatter = False
                continue
            if is_frontmatter and line.strip() != "":
                d = line.find(":")
                key = line[:d]
                value = line[d+1:].strip()
                if value[0] == '"' or value[0] == "'":
                    value = value[1:]
                if value[-1] == '"' or value[-1] == "'":
                    value = value[:-1]
                if value == "false":
                    value = False
                if value == "true":
                    value = True
                frontmatter[key] = value
            if line.startswith("**Veranstaltung:"):
                self.article_parts["event_date"] = line.replace("**","")
            elif line.startswith("Kalenderdatei:") and line.strip().endswith(".ics)"):
                
                self.article_parts["calendar"] = line
                self.article_parts["calendar_line"] = self.prepare_calender_line() + "\n"
            elif not is_frontmatter:
                content += line
        self.article_parts["frontmatter"] = frontmatter
        self.article_parts["content"] = content.replace("\n\n\n", "\n\n")

        return self.article_parts
        
    def get_img_lines(self):
        self.img_lines = []
        for line in self.article_parts["content"].split("\n"):
            if line.startswith("![") and line.endswith(")"):
                img_line = line.split("(")[1][:-1]
                limit = img_line.rfind("/") + 1
                img_dir = img_line[:limit]
                img_file = img_line[limit:]
                self.img_lines.append([img_file, img_dir])
        return self.img_lines

    def get_title(self):
        return self.article_parts["frontmatter"]["title"]
    
    def get_subtitle(self):
        return self.article_parts["frontmatter"]["subtitle"]

    def get_title_lines(self):
        return self.article_parts["frontmatter"]["title"] + "\n===========\n" + self.article_parts["frontmatter"]["subtitle"] + "\n"
    
    def get_event_line(self):
        return self.article_parts["event_date"]

    def prepare_calender_line(self):
        self.calendar_line = self.article_parts["calendar"].replace("Kalenderdatei:","").replace("[","").replace("]","").replace("(",": "+baseURL).replace(")","").strip() + "\n"
        return self.calendar_line


class SM_post():
    def __init__(self, Article=None):
        self.char_limit = 1000
        self.Article = Article
        if self.Article != None:
            self.frontmatter = self.Article.article_parts["frontmatter"]
            self.event = self.Article.article_parts["event_date"]
            self.calendar_line =  self.Article.article_parts["calendar_line"]
            self.content =  self.Article.article_parts["content"]
            try:
                self.publish = self.Article.article_parts["frontmatter"]["social_media"]
            except:
                self.publish = False
            self.title_lines = self.Article.get_title_lines()
            self.rel_url = self.get_rel_url()
        return

    def get_rel_url(self):
        if self.Article != None:
            return None
        url_line = self.Article.article_parts["frontmatter"]["URL"]
        return url_line.strip().replace('"','')

    def prepare_post(self):
        if self.Article != None:
            return None
        self.url_ref = baseURL + self.rel_url
        overhead = len(self.url_ref) + len(' ... mehr: ')
        self.post_content = self.event + "\n" +  self.calendar_line + "\n" +  self.content
        self.post_content = self.post_content[:self.char_limit - overhead]
        limit = max(self.post_content.rfind(". "),self.post_content.rfind("\n"))
        self.post_content = self.post_content[:limit+1]
        if self.rel_url != "":
            self.post_content += ' ... mehr: ' + self.url_ref
        return self.post_content
           
    def send_post(self):
        if self.Article != None:
            return None
        if not self.publish:
            return None
        self.post = self.prepare_post()
        if len(self.Article.img_lines) == 0:
            out = self.send_post_with_image()
            #out = self.send_post_without_image()
        else:
            out = self.send_post_with_image(ImgFDIR=self.Article.img_lines[0][1], img_file=self.Article.img_lines[0][0])
        return out


class mastodon_post(SM_post):
    def __init__(self, Article=None):
        self.char_limit = 500
        self.cred_fn = cred_fdir + "mastodon_uScw.json"
        self.cred = self.get_cred()
        self.token = self.cred["token"]
        self.api_base_url = self.cred["api_base_url"]
        self.m = Mastodon(access_token=self.token, api_base_url=self.api_base_url)
        self.Article = Article
        if Article != None:
            self.rel_url = self.get_rel_url()
            self.frontmatter = self.Article.article_parts["frontmatter"]
            self.event = self.Article.article_parts["event_date"]
            self.calendar_line =  self.Article.article_parts["calendar_line"]
            self.content =  self.Article.article_parts["content"]
            try:
                self.publish = self.Article.article_parts["frontmatter"]["social_media"]
            except:
                self.publish = False
            self.title_lines = self.Article.get_title_lines()
        return

    def send_post_without_image(self):
        if self.Article != None:
            return None
        print ("POST to Mastodon: " + self.post)
        ret = False
        if not no_posts:
            ret = self.m.toot(self.post)
        return ret
    
    def send_post_with_image(self, ImgFDIR=None, img_file=None):
        if self.Article != None:
            return None
        # for muliple images see: https://buerviper.github.io/blog/2024/writing-a-mastodon-bot-in-python/
        if img_file != None and not no_posts:
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
            self.image = self.m.media_post(img_file, mime_type = mtype, description = self.content )
            # this is the only required argument. you can either give the filename directly or use the "media_file" argument.
            # this indicates the filetype. only necessarily needed if you did not use "media_type", otherwise the program will guess the correct file type
            # adds alt text. you should definitely consider this!

        # Write a post with an image
        print ("POST to Mastodon: " + self.post + " WITH " + img_file)
        ret = False
        if not no_posts:
            ret = self.m.status_post(self.post, media_ids=self.image["id"] )
        # this is the text associated with the message
        # as said earlier, the media_post function uploads the image with an id as a dictionary. this calls the correct photo
        return ret

    def get_img_dir(self, img_line):
        if self.Article != None:
            return None
        img_ptr = img_line.split("(")[1][:-1]
        last_slash = img_ptr.rfind("/")
        img_prefix = img_ptr[:last_slash]
        img_file = img_ptr[last_slash:]
        return img_prefix, img_file
    
    def delete_post(self,id):
        return

    def get_cred(self):
        try:
            cred_file = open(self.cred_fn, "r")
            fjson = json.loads(cred_file.read())
        except:
            print (datetime.now().isoformat() + " " + "Error: Access Token for Mastodon not found at " + cred_fn + ". Try mounting the credentials file system")
            sys.exit(1)
        return fjson

    def get_token(self):
            return cred["token"]

    def lookup_account(self):
        return self.m.account_lookup(self.user)


class instagram_post(SM_post):
    def __init__(self,Article):
        self.char_limit = 200
        self.client = InstaClient()
        self.credfile = cred_fdir + "instagram_GoeKB.json"
        self.cred = self.get_credentials()
        self.user_md = self.server_login()
        # self.settings = self.lookup_account() 
        self.Article = Article
        if self.Article != None:
            self.rel_url = self.get_rel_url()
            self.frontmatter = self.Article.article_parts["frontmatter"]
            self.event = self.Article.article_parts["event_date"]
            self.calendar_line =  self.Article.article_parts["calendar_line"]
            self.content =  self.Article.article_parts["content"]
            try:
                self.publish = self.Article.article_parts["frontmatter"]["social_media"]
            except:
                self.publish = False
        return

    def get_credentials(self):
        try:
            fc = open(self.credfile)
            cred_str = fc.read()
        except:
            print(datetime.now().isoformat() + " " + "Error: credentials file for BlueSky not found at " + self.credfile + ". Try mounting the credentials file system")
            sys.exit(1)
        return eval(cred_str)

    def server_login(self):
        if not self.client.login(self.cred['username'], self.cred['password']):
            print ("Error: could not login with " + self.cred['username'] + " at " + self.cred["baseuri"])

    def lookup_account(self):
        return self.client.get_settings()

    def prepare_post(self):
        if self.Article != None:
            return None
        cal_parts = self.calendar_line.find(":")
        self.cal_text = self.calendar_line[:cal_parts]
        self.cal_url = self.calendar_line[cal_parts+1:].strip()
        self.url_ref = baseURL + self.rel_url
        overhead = len(self.event) + len(' ... mehr: ')
        self.post_content = self.content[:self.char_limit - overhead]
        # self.post_content = self.content[:self.char_limit]
        limit = max(self.post_content.rfind(". "),self.post_content.rfind("\n"))
        self.post_content = self.post_content[:limit+1]
        return self.post_content

    def send_post_without_image(self):
        # currently only posts with images are supported
        return None

        if self.Article != None:
            return None
        self.send_post_with_image(ImgFDIR=None, img_file=None)
        url = self.url_ref
        ts = self.post_content[-1].rfind("/")
        url_title = "... mehr"
        out = self.client.send_post(blueskyClientUtils.TextBuilder()
                                    .text(self.event)
                                    .link(self.cal_text, self.cal_url)
                                    .text(self.post_content)
                                    .link(url_title, url))
        self.client.like(out.uri, out.cid)        
        return out.uri + " " + out.cid
        return out
    
    def send_post_with_image(self, ImgFDIR=None, img_file=None):
        if self.Article != None:
            return None
        self.post = self.prepare_post()
        print ("POST to Instagram: " + self.post + " WITH " + img_file)
        ret = None
        if not no_posts:
            ret = cl.photo_upload(path=img_file, caption=self.post)
        return ret

class bluesky_post(SM_post):
    def __init__(self,Article):
        self.char_limit = 200
        self.Article = Article
        if self.Article != None:
            self.rel_url = self.get_rel_url()
            self.frontmatter = self.Article.article_parts["frontmatter"]
            self.event = self.Article.article_parts["event_date"]
            self.calendar_line =  self.Article.article_parts["calendar_line"]
            self.content =  self.Article.article_parts["content"]
            try:
                self.publish = self.Article.article_parts["frontmatter"]["social_media"]
            except:
                self.publish = False
        self.client = blueskyClient()
        self.credfile = cred_fdir + "bluesky_uScw.json"
        self.cred = self.get_credentials()
        self.user_md = self.server_login()
        return

    def get_credentials(self):
        try:
            fc = open(self.credfile)
            cred_str = fc.read()
        except:
            print(datetime.now().isoformat() + " " + "Error: credentials file for BlueSky not found at " + self.credfile + ". Try mounting the credentials file system")
            sys.exit(1)
        return eval(cred_str)

    def server_login(self):
        return self.client.login(self.cred['username'], self.cred['password'])

    def prepare_post(self):
        if self.Article != None:
            return None
        cal_parts = self.calendar_line.find(":")
        self.cal_text = self.calendar_line[:cal_parts]
        self.cal_url = self.calendar_line[cal_parts+1:].strip()
        self.url_ref = baseURL + self.rel_url
        overhead = len(self.event) + len(' ... mehr: ')
        self.post_content = self.content[:self.char_limit - overhead]
        # self.post_content = self.content[:self.char_limit]
        limit = max(self.post_content.rfind(". "),self.post_content.rfind("\n"))
        self.post_content = self.post_content[:limit+1]
        return self.post_content

    def send_post_without_image(self):
        if self.Article != None:
            return None
        post = self.prepare_post()
        url = self.url_ref
        ts = self.post_content[-1].rfind("/")
        url_title = "... mehr"        
        print ("POST to Instagram: " + self.post_content)
        ret = None
        if not no_posts:
            out = self.client.send_post(blueskyClientUtils.TextBuilder()
                                    .text(self.event)
                                    .link(self.cal_text, self.cal_url)
                                    .text(self.post_content)
                                    .link(url_title, url))
            self.client.like(out.uri, out.cid)        
            ret = out.uri + " " + out.cid
        return ret
    
    def send_post_with_image(self, ImgFDIR=None, img_file=None):
        if self.Article != None:
            return None
        ret = self.send_post_without_image()        
        if img_file != None:
            if ImgFDIR == None or ImgFDIR == "":
                ImgFDIR = eventImgFDIR 
            img_file = ImgFDIR + img_file
            print ("POST image to Instagram: " + img_file)
            ret = None
            if not no_posts:
                with open(img_file, 'rb') as img:
                    img_data = img.read()
                    self.client.send_image(text='', image=img_data, image_alt=self.event)
        return ret
        

    def prepare_external_link(self):
        external_link = AppBskyEmbedExternal.External(uri=URL, title=URL_TITLE, description=URL_DESCRIPTION)
        return url, url_title, url_description, external_link
        

class schoenerleben_post(SM_post):
    def __init__(self, Article):
        self.char_limit = 500
        self.Article = Article
        self.frontmatter = self.Article.article_parts["frontmatter"]
        self.subject = self.get_subject()
        self.event = self.Article.article_parts["event_date"]
        self.calendar_line =  self.Article.article_parts["calendar_line"]
        self.content =  self.Article.article_parts["content"]
        try:
            self.publish = self.Article.article_parts["frontmatter"]["social_media"]
        except:
            self.publish = False
        self.rel_url = self.get_rel_url()
        self.credfile = cred_fdir + "mail_ionos_GoeKB.json"
        self.receivers = schoenerleben_receivers
        self.cred = self.get_credentials()
        # self.To_Send_Folder = True
        return

    def get_credentials(self):
        try:
            fc = open(self.credfile)
            cred_str = fc.read()
        except:
            print(datetime.now().isoformat() + " " + "Error: credentials file for SchoenerLeben not found at " + cred_fn + ". Try mounting the credentials file system")
            sys.exit(1)
        return eval(cred_str)

    def get_subject(self):
        self.subject = self.Article.get_event_line() + " - " + self.Article.get_title()
        return self.subject
    
    def send_post_without_image(self):
        self.rel_url
        post = self.prepare_post()
        subject = self.get_subject()
        # body = self.content
        print ("POST to SchoenerLeben: " + subject + ":\n" + post)
        ret = None
        if not no_posts:
            out = self.send_email(subject, post)
        return out

    def send_post_with_image(self, ImgFDIR=None, img_file=None):
        # cannot send any images to schoenerleben right now
        return self.send_post_without_image()


    def send_email(self,subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.cred["username"]
        msg['To'] = ', '.join(self.receivers)
        self.username = self.cred["username"]
        self.password = self.cred["password"]
        self.smtpserver = self.cred["baseuri"].split(":")[0]
        self.smtpport = int(self.cred["baseuri"].split(":")[1])
        self.imapserver = self.cred["imapuri"].split(":")[0]
        self.imapport = int(self.cred["imapuri"].split(":")[1])
        self.imapport = 993

        try:
            with smtplib.SMTP(self.smtpserver, self.smtpport) as smtp_server:
                smtp_server.starttls()  # Start TLS encryption
                smtp_server.login(self.username, self.password)
                smtp_server.sendmail(self.username, self.receivers, msg.as_string())
                out = "The event email is sent from: " + self.username + " successfully to: " + ', '.join(self.receivers)
        except:
            out = "Error: The event email from: " + self.username + "  to: " + ', '.join(self.receivers) + " failed"
        # if self.To_Send_Folder:
        #     self.move_to_send_folder(msg)
        return out

    def move_to_send_folder(self,msg):
        imap = imaplib.IMAP4_SSL(self.imapserver, self.imapport)
        imap.login(self.username, self.password)
        imap.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(datetime.now().timestamp()), msg.as_string().encode('utf8'))
        return imap.logout()
        

def post_all_with_timedelta(timedelta):
    dt_tdelta = datetime.strftime(datetime.now()+timedelta(days=timedelta),"%Y-%m-%d")
    
    for file in os.listdir(eventFDIR):

        if file.startswith(dt_tdelta) and not file.endswith("~"):
            ff = open(eventFDIR + file)
            article_lines = ff.readlines()
            Article = article(article_lines)           
            # print (Article.article_parts)
            # content = Article.article_parts["content"]
            post_article(Article)
            
def post_article(Article):
        frontmatter = Article.article_parts["frontmatter"]
        try:
            if not post_forced and not frontmatter["social_media"]:
                print (datetime.now().isoformat() + " " + "for item: " + eventFDIR + file + "\nno publication wanted by frontmatter: 'social_media:false'")
                sys.exit(0)
        except: 
            print ("for item: " + eventFDIR + file + "\nno publication wanted by frontmatter")
            sys.exit(0)


        Instagram_Post = instagram_post(Article)
        out = Instagram_Post.send_post()
        out = str(datetime.now().isoformat()) + " " + str(out)[:out_lg]
        print(out)

        Mastodon_Post = mastodon_post(Article)
        out = Mastodon_Post.send_post()
        out = str(datetime.now().isoformat()) + " " + str(out)[:out_lg]
        print(out)

        BlueSky_Post = bluesky_post(Article)
        out = BlueSky_Post.send_post()
        out = str(datetime.now().isoformat()) + " " + str(out)[:out_lg]
        print(out)

        SchoenerLeben_Post = schoenerleben_post(Article)
        out = SchoenerLeben_Post.send_post()
        out = str(datetime.now().isoformat()) + " " + str(out)[:out_lg]
        print(out)

##########################
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        ff = open(eventFDIR + file)
        article_lines = ff.readlines()
        Article = article(article_lines)           
        # print (Article.article_parts)
        # content = Article.article_parts["content"]
        post_article(Article)

