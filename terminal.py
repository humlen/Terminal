"""
@created: Sun Feb 5 17:06:42 2023
@author: eirik

@purpose: act as a terminal launcher for all MSMF Protocols
"""
import time
time_launch = time.time()


import sys
import os
import warnings

from src import splash # type: ignore
import msvcrt as m

# HACK: Lazy loading Eidos, Lantern and Terra to boost
# startup time. Change this to multithreaded loading 
# instead.


# Get help from other worlds
sys.path.append("..")
# from Confidential.datacollection import terra # type: ignore

# Classic
warnings.filterwarnings("ignore")

# Name & Version
VERSION_NAME = "Terminal"
VERSION_NUMBER = "1.0"
COLOR_OPEN = "\x1b["
COLOR_CLOSE = "\x1b[0m"
COLOR_ORANGE = "0;33;40m"
COLOR_GREEN = "0;32;40m"


# Initialize
item1 = "0"

# Home Screen 
while True:

     # Initialize Screen
    from src.splash import print_splash
    os.system('cls')
    print_splash()
    print(VERSION_NAME+" "+VERSION_NUMBER)
    print('Startup Time: '+str(round((time.time() - time_launch),3))+' Seconds')
    
    item1 = input("""\nWhat program would you like to try?\n
        """+COLOR_OPEN+COLOR_ORANGE+"""Project Terra"""+COLOR_CLOSE+"""
        1. Terra Nova
        2. Terra
        3. Terra Erdos
    
       """+COLOR_OPEN+COLOR_ORANGE+"""Project Spotlight"""+COLOR_CLOSE+"""
        4. Spotlight Search
   
        """+COLOR_OPEN+COLOR_ORANGE+"""Project Eidos"""+COLOR_CLOSE+"""
        5. Eidos Ranker
        6. Eidos Test
    
        """+COLOR_OPEN+COLOR_ORANGE+"""Other"""+COLOR_CLOSE+"""
        0. Info\n
        Q. Quit\n""")
         
    
# Terra Nova
    while item1 == "1":

       # Initialize Screen
        os.system('cls')
        print_splash()
        
        # Import & Execute desired programfrom
        from Confidential.datacollection import terra # type: ignore
        item2 = input(""" \nWhat do you want your sample size to be\n""")
        item2_int = int(item2)
        print("\nrunning Terra Nova Protocol with "+item2+" samples")
        terra.terra_nova(item2_int)
        print('\nPress Q to exit')
        keypress = m.getch()
        if  keypress == 'q':
            item1 = "0"
        break


# Terra
    while item1 == "2":

        # Initialize Screen
        os.system('cls')
        print_splash()

        # Import & Execute desired program
        from Confidential.datacollection import terra # type: ignore
        item2 = input(""" \nWhat metric would you like to collect?\n
        1. Revenue
        2. Net Income
        3. EPS
        4. All Four
        
        Q. Return\n""")
        print("\nrunning Terra Protocol for "+item2)
        if item2 in ("1", "2", "3", "4"):
            if item2 == "1":
                terra.prima_terra("Revenue")
        
                # Exit state
                print('\nPress Q to exit')
                keypress = m.getch()
                if  keypress == 'q':
                    item1 = "0"
                break
            if item2 == "2":
                terra.prima_terra("Net Income")
                # Exit state
                print('\nPress Q to exit')
                keypress = m.getch()
                if  keypress == 'q':
                    item1 = "0"
                break
            if item2 == "3":
                terra.prima_terra("EPS")
                # Exit state
                print('\nPress Q to exit')
                keypress = m.getch()
                if  keypress == 'q':
                    item1 = "0"
                break
            if item2 == "4":
                terra.prima_terra("Revenue")
                terra.prima_terra("Net Income")
                terra.prima_terra("EPS")
                # Exit state
                print('\nPress Q to exit')
                keypress = m.getch()
                if  keypress == 'q':
                    item1 = "0"
                break
        elif item2 == 'q':
            item1 = '0'
        else:
            print("\nThe Terra Protocol does not support this metric currently.")
        break


    # Terra Erdos
    # FIX: Currently broken 
    while item1 == "3":
        from Confidential.datacollection import terra # type: ignore
        print("\n Running Terra Error Protocol")
        terra.terra_errors()
        break

    # Project Spotlight 
    while item1 == "4":
        
        # Initialize Screen
        os.system('cls')
        print_splash() 
        
        # Import & Execute desired program
        from src import spotlight 
        item2 = input("\nWhat ticker would you like to retrieve\n")
        spotlight.illuminate(item2)

        # Exit state
        print('\nPress Q to exit')
        keypress = m.getch()
        if  keypress == 'q':
            item1 = "0"
        break
        

# Project Eidos
    while item1 == "5":
       
        # Initialize Screen
        os.system('cls')
        print_splash()
        
        # Import & Execute desired program
        from src import eidos
        item2 = input("""\nWhat metric would you like to rank by?
        1. Revenue
        2. Net Income
        3. Earnings Per Share\n""")
        if item2 == "1":
            eidos.eidos_revenue()
            # Exit state
            print('\nPress Q to exit')
            keypress = m.getch()
            if  keypress == 'q':
                item1 = "0"
            break
        if item2 == "2":
            eidos.eidos_netinc()
            # Exit state
            print('\nPress Q to exit')
            keypress = m.getch()
            if  keypress == 'q':
                item1 = "0"
            break
        if item2 == "3":
            eidos.eidos_eps()
            # Exit state
            print('\nPress Q to exit')
            keypress = m.getch()
            if  keypress == 'q':
                item1 = "0"
            break
     
    while item1 == "6":
        
        # Initialize Screen
        os.system('cls')
        print_splash()
        
        # Import & Execute desired program
        from src import eidos
        eidos.eidos_test() 
       
        # Exit state
        print('\nPress Q to exit')
        keypress = m.getch()
        if  keypress == 'q':
            item1 = "0"
        break
# Info
    while item1 == "9":
       
        # Initialize Screen
        os.system('cls')
        print_splash()
        
        # Import & Execute desired program
        from src import lantern, eidos
        from Confidential.datacollection import terra
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
        
        # Exit state
        print('\nPress Q to exit')
        keypress = m.getch()
        if  keypress == 'q':
            item1 = "0"
        break

    while item1 == 'q':
        quit()
