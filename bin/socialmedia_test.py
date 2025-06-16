#!/usr/bin/python3
import os
import sys
import json

# Import the Client class for Mastodon
from mastodon import Mastodon
# Import the Client class for Bluesky from the atproto library
from atproto import Client as blueskyClient
from atproto import client_utils as blueskyClientUtils
# Import the Client class for Instagram
from instagrapi import Client as InstaClient

cred_fdir = "/tmp/Certs/otherCredentials/"

class SM_post():
    def __init__(self):
        return
    def send_request(self):
        posts = get_posts()
        return posts


class instagram_post(SM_post):
    def __init__(self):
        self.client = InstaClient()
        self.credfile = cred_fdir + "instagram_GoeKB.json"
        self.cred = self.get_credentials()
        self.user_md = self.server_login()
        # self.settings = self.lookup_account() 
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



class bluesky_post(SM_post):
    def __init__(self):
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

    
class mastodon_post(SM_post):
    def __init__(self):
        self.cred_fn = cred_fdir + "mastodon_uScw.json"
        self.cred = self.get_cred()
        self.token = self.cred["token"]
        self.api_base_url = self.cred["api_base_url"]
        self.user = self.cred["client_name"]
        self.m = Mastodon(access_token=self.token, api_base_url=self.api_base_url)
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

    
##########################
if __name__ == '__main__':
    M = mastodon_post()
    settings = M.lookup_account()
    print ("Mastodon Id: " + str(settings["id"]))

    B = bluesky_post()
    print("BlueSky Id: " + str(B.user_md["did"]))

    I = instagram_post()
    settings = I.lookup_account()
    print ("Instagram Id: " + str(settings['authorization_data']['ds_user_id']))
