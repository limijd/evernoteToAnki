#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#API reference: https://dev.evernote.com/doc/reference/NoteStore.html

import os
import sys
import json

SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/evernote/lib"%SCRIPT_PATH)

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as ns_ttypes
from evernote.api.client import EvernoteClient

class NotebookReader:
    def __init__(self, notebook_name):
        self.notebook_name = notebook_name
        self.token = self.readToken()
        assert self.token

        self.ev_client = None
        self.ev_note_store = None
        self.ev_notebook = None
        self.ev_notes_metadata = []
        self.ev_notes = {}

        self.clientConnect()
        self.fetchNotesMetadata()
        return

    def readToken(self):
        token_file = os.path.expanduser("~/.evernote_token.json")
        with open(token_file, "r") as fp:
            js = json.load(fp)
            assert "token" in js
            token = js["token"]
            return token
        return None


    def clientConnect(self):
        self.ev_client = EvernoteClient(token=self.token, sandbox=False, china=False)
        self.ev_note_store = self.ev_client.get_note_store()
        notebooks = self.ev_note_store.listNotebooks()
        for nb in notebooks:
            if nb.name == self.notebook_name:
                self.ev_notebook = nb


    def fetchNotesMetadata(self):
        flt = ns_ttypes.NoteFilter()
        flt.notebookGuid = self.ev_notebook.guid
        rs = ns_ttypes.NotesMetadataResultSpec()
        rs.includeTitle = True
        nml = self.ev_note_store.findNotesMetadata(self.token, flt, 0, 10000, rs)
        for n in nml.notes:
            self.ev_notes_metadata.append([n.guid, n.title])

        return

if __name__ == "__main__":
    nr = NotebookReader("AnkiQuickNotes")
    for n in nr.ev_notes_metadata:
        print n[0], n[1]
