"""
Splash screen for the terminal
"""


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


def print_splash(): 
    print(LOGO)

