#!/usr/bin/env python3
"""My ngl clone lamo."""


import flask
import time, os, json, csv

class nglxD:
    """My ngl clone lol"""

    def __init__(self) -> None:
        """Load diff data sources."""
        self.appleD = json.load(open('pple_ids.json', 'r'))
        self.androidD = json.load(open('andr_ids.json', 'r'))


