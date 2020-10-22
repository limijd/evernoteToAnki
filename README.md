# Evernote to ANKI

Create ANKI cards from Evernote notebook

## Description

Read notes from a given evernote notebook. Create ANKI import file with three fields: title, content, tags

HTML note also works perfectly.

## Setup

* You need to obtain an Evernote developer token. It disabled by default. Need to ask customer service to enable.


## Usage

```
usage: eta.py [-h] [-d] [-nb NOTEBOOK] [-o OUT]

eta: Evernote to Anki

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           debug mode
  -nb NOTEBOOK, --notebook NOTEBOOK
                        Evernote notebook to be read
  -o OUT, --out OUT     output file for importing to ANKI
```
