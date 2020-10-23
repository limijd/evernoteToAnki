#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#API reference: https://dev.evernote.com/doc/reference/NoteStore.html

import os
import sys
import re
import json
import argparse
import logging

SCRIPT_PATH=os.path.dirname(os.path.realpath(__file__))
sys.path.append("%s/evernote/lib"%SCRIPT_PATH)

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as ns_ttypes
from evernote.api.client import EvernoteClient
#from bs4 import BeautifulSoup

ANKI_CONTENT_LIMIT = 131072

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

        self.ev_tags = {} #guid:tag map

        self.clientConnect()
        self.fetchNotesMetadata()
        self.fetchTags()
        self.fetchNotes()
        return

    def readToken(self):
        token_file = os.path.expanduser("~/.evernote_to_anki.config.json")
        with open(token_file, "r") as fp:
            js = json.load(fp)
            assert "token" in js
            token = js["token"]
            return token
        return None


    def clientConnect(self):
        logging.info("Connect to Evernote...")
        self.ev_client = EvernoteClient(token=self.token, sandbox=False, china=False)
        self.ev_note_store = self.ev_client.get_note_store()
        notebooks = self.ev_note_store.listNotebooks()
        logging.info("Read all notebooks")
        for nb in notebooks:
            if nb.name == self.notebook_name:
                self.ev_notebook = nb

    def fetchTags(self):
        logging.info("Read all tags")
        for tag_guid in self.ev_tags.keys():
            tag = self.ev_note_store.getTag(self.token, tag_guid)
            self.ev_tags[tag_guid] = tag.name

    def fetchNotesMetadata(self):
        logging.info("Getting metadata from notebook: %s", self.notebook_name)
        flt = ns_ttypes.NoteFilter()
        flt.notebookGuid = self.ev_notebook.guid
        rs = ns_ttypes.NotesMetadataResultSpec()
        rs.includeTitle = True
        rs.includeTagGuids = True
        nml = self.ev_note_store.findNotesMetadata(self.token, flt, 0, 10000, rs)
        for n in nml.notes:
            #n is "NoteMetadata" type
            self.ev_notes_metadata.append([n.guid, n.title])
            if n.tagGuids:
                for t in n.tagGuids:
                    self.ev_tags[t] = None
            else:
                logging.info("No Tag found for: %s ", n.title)
        return

    def fetchNotes(self):
        logging.info("Getting notes content from notebook: %s", self.notebook_name)
        for guid, title in self.ev_notes_metadata:
            rs = ns_ttypes.NoteResultSpec()
            logging.debug("fetching note: %s",title)
            rs.includeContent = True #ENML contents
            note = self.ev_note_store.getNoteWithResultSpec(self.token, guid, rs)
            assert title==note.title
            #self.beautifyContent(note.content)
            content = self.processNoteContent(note.content)
            self.ev_notes[note.contentHash] = [title, note.tagGuids, note.contentHash, content]

    def processNoteContent(self, content):
        content = re.sub(r'\t', '  ', content)
        content = re.sub(r'\n', '<br>', content)
        search = re.search(r'<en-note>.*</en-note>', content, flags=re.UNICODE)
        if not search:
            return content
        else:
            return search.group(0)

    def writeAnkiImportTextFile(self, fn):
        logging.info("Export %d notes from %s to ANKI import file: %s", len(self.ev_notes), self.notebook_name, fn)
        fp = open(fn, "w")

        for note in self.ev_notes.values():
            tags = []
            if note[1]:
                for guid in note[1]:
                    tag_name = self.ev_tags[guid]
                    tags.append(tag_name)
            tag = " ".join(tags)  #ANKI uses space to separate tags


            global ANKI_CONTENT_LIMIT
            if len(note[3]) > int(ANKI_CONTENT_LIMIT*0.8):
                logging.info("Skip note because content too long for ANKI: %s", note[0])
                continue

            fp.write("%s\t"%note[0].encode("utf-8"))
            fp.write("%s\t"%note[3].encode("utf-8"))
            fp.write("%s\n"%tag)
        fp.close()

    #def beautifyContent(self, content):
    #    soup = BeautifulSoup(content)
    #    print(soup.get_text())
    #    return

def main():
    """ entry of program """
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__)
            , description="eta: Evernote to Anki")
    parser.add_argument('-d', '--debug', action='store_true', help="debug mode")
    parser.add_argument('-nb', '--notebook', default='AnkiQuickNotes', help="Evernote notebook to be read")
    parser.add_argument('-o', '--out', default='anki.import.txt', help="output file for importing to ANKI")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='[eta: %(asctime)s %(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    else:
        logging.basicConfig(format='[eta: %(asctime)s %(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

    nr = NotebookReader(args.notebook)
    nr.writeAnkiImportTextFile(args.out)

    logging.info("Evernote to ANKI completed successfully.")

if __name__ == "__main__":
    main()
