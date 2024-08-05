#!/usr/bin/env python3
"""My ngl clone lamo."""


import flask
import time, os, json, csv, uuid
from ua_parser import user_agent_parser as uap

class nglxD:
    """My ngl clone lol"""

    def __init__(self) -> None:
        """Load diff data sources."""
        self.appleD = json.load(open('pple_ids.json', 'r'))
        self.androidD = json.load(open('andr_ids.json', 'r'))
        self.appleHelp = ["apple", "ipod", "macbook", "mac mini", "mac", "macpro", "imac"]
        self.users = {}

    def break_ua(self, ua):
        """Break down ua and give os type."""
        # user_agent_parser.Parse(ua)['user_agent']['family'] 'Instagram'
        # user_agent_parser.Parse(ua)['os']['family'] 'iOS' 'Android' 'Linux' 'Windows' 'Mac OS X'
        # user_agent_parser.Parse(ua)['device']['model'] 'M2101K6G' 'iPhone15,3' 'iPad13,4' 'Mac'
        # is all apple devices detected as 'iOS'?????????????????
        # try user_agent_parser.Parse(ua)['device']['family'].split(" Build")[0]
        # no model in android???? take family as model user_agent_parser.Parse(ua)['device']['family']
        # test for macos stuff
        os = None
        name = None
        from_instagram = False
        u = uap.Parse(ua)
        os = u['os']['family']
        model = u['device']['model']
        brand = u['device']['brand']
        if u['user_agent']['family'] == 'Instagram' or "instgram" in ua.lower():
            from_instagram = True
        if os == "Android":
            if model:
                try:
                    name = self.androidD[model]['Marketing Name']
                    brand = self.androidD[model]['Retail Branding']
                except KeyError:
                    try:
                        model = u['device']['family'].split(" Build")[0]
                        name = self.androidD[model]['Marketing Name']
                        brand = self.androidD[model]['Retail Branding']
                    except:
                        name = u['device']['family'].split(" Build")[0]
            else:
                name = u['os']['family'] + " " + u['os']['major']
        elif os == "iOS":
            brand = "Apple"
            if model:
                try:
                    name = self.appleD[model][0]
                except KeyError:
                    name = "unkn Apple " + model
            else:
                name = "unkn Apple iPhone"
        elif os == "Windows":
            brand = "Microsoft"
            name = "Windows "
            # win ver logic
        elif os == "Mac OS X":
            brand = "Apple"
            try:
                name = self.appleD[model][0]
            except:
                name = "Apple " + model
        elif os == "Linux":
            name = u['device']['family']
            brand = "Linux"
        else:
            for x in self.appleHelp:
                if x in ua.lower():
                    brand = "Apple"
                    try:
                        name = self.appleD[model][0]
                    except:
                        pass

        return self.save_me(name, brand, from_instagram, ua)
                        
    def save_me(self, name, brand, insta, ua):
        """SAve in DB."""
        idd = uuid.uuid4
        d = {
            "name": name,
            "brand": brand,
            "isInsta": insta,
            "ua": ua
        }
        self.users[idd] = d
        return idd

    def get_me(self, idd):
        """Query db."""
        return self.users[idd]
