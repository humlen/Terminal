# Project Terminal

## Introduction

The mainframe through which all MSMF projects will be launched through.

## Changelog

### Version: 1.1 [Live]

---
_Release Date: 2023-07-28_

#### Comments
Moved entire build to a portable version, and forced to run
on Python 3.8 with pipenv. Lazy loads packages for improved 
performance. Sped up Ranking algorithm and expanded diagnostics.

#### General
+ remade folder structure into Codebase
+ added relative pathing for multi-platform use

#### Terminal
+ added startup timer for terminal.py
+ aesthetic changes to clearing
+ moved splash to separate function
+ changed imports to load lazily

#### Eidos
+ added feedback to eidos calculations
+ rewrote pearson and spearman to 2.2k it/s 
+ added Kendalls Tau to Project eidos
+ now prints top 10 companies of each sector
+ Added equity count and filters to diagnostics

#### Lantern
+ added final timer to lantern fetch
+ moved macrotrends scrape and formatting to function
+ added relative valuation

### Version: 1.0 

---
_Release Date: 2023-04-22_

+ Just been doodling up until this point so I guess the changelog starts here.
