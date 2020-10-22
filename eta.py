#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import json

SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/evernote/lib"%SCRIPT_PATH)

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

token_file = os.path.expanduser("~/.evernote_token.json")
token = None

with open(token_file, "r") as fp:
    js = json.load(fp)
    token = js["token"]

assert token


#sandbox=False means use production service with Developer token
client = EvernoteClient(token=token, sandbox=False, china=False)

note_store = client.get_note_store()

notebooks = note_store.listNotebooks()
for nb in notebooks:
    print "notebook: ", nb.name
