#!/usr/bin/env python3
"""My ngl clone lamo."""


import flask
import time, os, json, csv, uuid
from ua_parser import user_agent_parser as uap
from typing import List

class nglxD:
    """My ngl clone lol"""

    def __init__(self) -> None:
        """Load diff data sources."""
        self.appleD = json.load(open('pple_ids.json', 'r'))
        self.androidD = json.load(open('andr_ids.json', 'r'))
        self.appleHelp = ["apple", "ipod", "macbook", "mac mini", "mac", "macpro", "imac"]
        self.users = self._load_users()

    def _load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", 'r') as file:
                return json.load(file)
        return {}

    def _save_users(self):
        with open("users.json", 'w') as file:
            json.dump(self.users, file, indent=4)

    def break_ua(self, ua, winver=None):
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
        print(u)
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
            if winver:
                x = winver.split('.')[0].replace("\"", '')
                print(x, type(x))
                winver = int(x)
                if winver > 13:
                    name += '11'
                else:
                    name += '10'
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
        elif 'crkey' in ua.lower():
            name = u['os']['family']
            brand = 'Google' if not brand else brand
            print('HEREE', name)
            
        else:
            for x in self.appleHelp:
                if x in ua.lower().replace('applewebkit', ''):
                    brand = "Apple"
                    print("despert", x)
                    try:
                        name = self.appleD[model][0]
                    except:
                        pass

        return self.save_me(name, brand, from_instagram, ua)

    def save_me(self, name, brand, insta, ua) -> uuid.UUID:
        """SAve in DB."""
        idd = str(uuid.uuid4())
        d = {
            "name": name,
            "brand": brand,
            "isInsta": insta,
            "ua": ua
        }
        print(d)
        self.users[idd] = d
        self._save_users()
        return idd

    def get_me(self, idd) -> List:
        """Query db."""
        return self.users[idd]

    def print_all(self) -> None:
        """Show db."""
        for x in self.users:
            print(self.users[x])
            print()

x = nglxD()
# b = x.break_ua("Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.192 Mobile/15E148 Safari/604.1")
# print(b)
# b = x.break_ua("Mozilla/5.0 (Linux; Android 13; 22031116BG Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.81 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/475.1.0.46.82;]")
# print(b)
# b = x.break_ua("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10 GD")
# print(b)
# b = x.break_ua("Mozilla/5.0 (iPad; CPU OS 17_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/21A360 [FBAN/FBIOS;FBAV/469.0.0.36.102;FBBV/612967364;FBDV/iPad13,4;FBMD/iPad;FBSN/iPadOS;FBSV/17.0.3;FBSS/2;FBID/tablet;FBLC/zh_TW;FBOP/5;FBRV/617002225]")
# print(b)
# b = x.break_ua("Mozilla/5.0 (iPad; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22A5307i Instagram 339.0.3.12.91 (iPad13,4; iPadOS 18_0; nl_NL; nl; scale=2.00; 750x1334; 619461904; IABMV/1)")
# print(b)
# b = x.break_ua("Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20B110 Instagram 309.1.1.28.108 (iPhone15,3; iOS 16_1_2; en_US; en; scale=3.00; 1290x2796; 537288535)")
# print(b)
# b = x.break_ua("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 [ip:151.44.92.160]")
# print(b)
# b = x.break_ua("Mozilla/5.0 (Linux; Android 6.0.1; SM-N910F Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 Instagram 37.0.0.21.97 Android (23/6.0.1; 640dpi; 1440x2560; samsung; SM-N910F; trlte; qcom; pt_PT; 98288242)")
# print(b)
# print()
# x.print_all()

b = x.break_ua("Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666 Edg/127.0.0.0")
print(b)