"""
@created: Sun Feb 5 17:06:42 2023
@author: eirik

@purpose: act as a terminal launcher for all MSMF Protocols
"""
import sys
import os
import warnings
from src import lantern, eidos

# Get help from other worlds
sys.path.append("..")
from Confidential.datacollection import terra # type: ignore

# Classic
warnings.filterwarnings("ignore")

# Name & Version
VERSION_NAME = "Terminal"
VERSION_NUMBER = "1.0"
COLOR_OPEN = "\x1b["
COLOR_CLOSE = "\x1b[0m"
COLOR_GREEN = "0;32;40m"
COLOR_ORANGE = "0;33;40m"
COLOR_RED = "0;31;40m"
COLOR_BLUE = "0;34;40m"
COLOR_WHITE = "0;37;40m"
COLOR_SPECIAL_COMMAND = "3;37;40m"

LOGO = """
====================================================================="""+COLOR_OPEN+COLOR_ORANGE+"""

88888888888                             d8b                   888 
    888                                 Y8P                   888 
    888                                                       888 
    888   .d88b.  888d888 88888b.d88b.  888 88888b.   8888b.  888 
    888  d8P  Y8b 888P"   888 "888 "88b 888 888 "88b     "88b 888 
    888  88888888 888     888  888  888 888 888  888 .d888888 888 
    888  Y8b.     888     888  888  888 888 888  888 888  888 888 
    888   "Y8888  888     888  888  888 888 888  888 "Y888888 888 
                                                                  
"""+COLOR_CLOSE+"====================================================================="+"\n"


# Home Screen
print(LOGO)
print(VERSION_NAME+" "+VERSION_NUMBER)


item1 = input("""\nWhat program would you like to try?\n
    """+COLOR_OPEN+COLOR_ORANGE+"""Project Terra"""+COLOR_CLOSE+"""
    1. Terra Nova
    2. Terra
    3. Terra Erdos

    """+COLOR_OPEN+COLOR_ORANGE+"""Project Lantern"""+COLOR_CLOSE+"""
    4. Lantern Fetch

    """+COLOR_OPEN+COLOR_ORANGE+"""Project Eidos"""+COLOR_CLOSE+"""
    5. Eidos Ranker
    
    """+COLOR_OPEN+COLOR_ORANGE+"""Other"""+COLOR_CLOSE+"""
    0. Info\n""")


# Terra Nova
if item1 == "1":
    os.system('cls')
    item2 = input(""" \nWhat do you want your sample size to be\n""")
    item2_int = int(item2)
    print("\nrunning Terra Nova Protocol with "+item2+" samples")
    terra.terra_nova(item2_int)


# Terra
elif item1 == "2":
    os.system('cls')
    item2 = input(""" \nWhat metric would you like to collect?\n
    1. Revenue
    2. Net Income
    3. EPS
    4. All Four\n""")
    print("\nrunning Terra Protocol for "+item2)
    if item2 in ("1", "2", "3", "4"):
        if item2 == "1":
            terra.prima_terra("Revenue")
        if item2 == "2":
            terra.prima_terra("Net Income")
        if item2 == "3":
            terra.prima_terra("EPS")
        if item2 == "4":
            terra.prima_terra("Revenue")
            terra.prima_terra("Net Income")
            terra.prima_terra("EPS")
    else:
        print("\nThe Terra Protocol does not support this metric currently.")


# Terra Erdos
elif item1 == "3":
    print("\n Running Terra Error Protocol")
    terra.terra_errors()


# Project Lantern
elif item1 == "4":
    os.system('cls')
    item2 = input("\nWhat ticker would you like to retrieve\n")
    lantern.illuminate(item2)


# Project Eidos
elif item1 == "5":
    os.system('cls')
    item2 = input("""\nWhat metric would you like to rank by?
    1. Revenue
    2. Net Income
    3. Earnings Per Share\n""")
    if item2 == "1":
        eidos.eidos_revenue()
    if item2 == "2":
        eidos.eidos_netinc()
    if item2 == "3":
        eidos.eidos_eps()


# Info
elif item1 == "0":
    os.system('cls')
    print("""
    """+COLOR_OPEN+COLOR_GREEN+f"Welcome to {VERSION_NAME} {VERSION_NUMBER}"
    +COLOR_CLOSE+"""\n Here is some information about the respective tools available in this app:
    
    """+COLOR_OPEN+COLOR_GREEN+"""Terra Nova:"""+COLOR_CLOSE)
    print("    "+str(terra.terra_nova.__doc__)+"\n")

    print("    "+COLOR_OPEN+COLOR_GREEN+"Prima Terra:"+COLOR_CLOSE)
    print("    "+terra.prima_terra.__doc__+"\n") # type: ignore

    print("    "+COLOR_OPEN+COLOR_GREEN+"Terra Erdos:"+COLOR_CLOSE)
    print("    "+terra.terra_errors.__doc__+"\n") # type: ignore

    print("    "+COLOR_OPEN+COLOR_GREEN+"Illuminate:"+COLOR_CLOSE)
    print("    "+str(lantern.illuminate.__doc__))

    print("    "+COLOR_OPEN+COLOR_GREEN+"Eidos:"+COLOR_CLOSE)
    print("    "+eidos.__doc__)
    print("")

# Invalid Character
else:
    os.system('cls')
    print("\nSozzle ma brozzle, canny do that")
