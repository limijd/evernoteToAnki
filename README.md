# Evernote to ANKI

Create ANKI cards from Evernote notebook

## Description

Read notes from a given evernote notebook. Create ANKI import file with three fields: title, content, tags

HTML note also works perfectly.

## Setup

* An Evernote developer token is required. Since it's disabled by default now, you can just ask Evernote customer service to enable it.
* Install evernoteToAnki and evernote API

```
%> git clone /Users/wli/dev-sandbox/limijd.github/evernoteToAnki
%> cd evernoteToAnki
%> git submodule init
%> git submodule update
```

* Install any required Python module if "eta.py" can't run

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

## other
