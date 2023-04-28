"""
Docstring for Terminal 2.0
"""

import curses
from curses.textpad import Textbox, rectangle
from src.lantern import illuminate

__filename__ = 'Project Terminal'
__fileversion__ = '1.0'

menu = [
    'Project Lantern [WIP]',
    'Project Eidos [WIP]',
    'Project Terra [WIP]',
    'More Info', 
    'Exit'
]

def print_border(stdscr):
    
    sh, sw = stdscr.getmaxyx()

    # Draw Borders
    curses.curs_set(0) #type: ignore
     
    border_y = sh-1
    border_x = sw-2

    for i in range (1, border_y):
         stdscr.addstr(i, 0, "│")
         stdscr.addstr(i, border_x, "│")

    # Horizontal Borders
    for i in range (1, border_x):
        stdscr.addstr(0, i, "─")
        stdscr.addstr(border_y, i, "─")

    # Corners
    stdscr.addstr(0, 0, "╭")
    stdscr.addstr(0, border_x, "╮")
    stdscr.addstr(border_y, 0, "╰")
    stdscr.addstr(border_y, border_x, "╯")

    # Title
    stdscr.attron(curses.color_pair(5)) #type: ignore
    stdscr.addstr(0,2, f" {__filename__} v{__fileversion__} ")
    stdscr.attroff(curses.color_pair(5)) #type: ignore
    stdscr.refresh()

def print_menu_main(stdscr, selected_row_idx):
    stdscr.clear()

    for idx, row in enumerate(menu):
        x = 4 
        y = 4 + len(menu)+idx

        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1)) #type: ignore
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1)) #type: ignore
        
        else:
            stdscr.addstr(y,x,row)

    stdscr.refresh()


    
def print_menu_lantern(stdscr):
    
    stdscr.clear()
    print_border(stdscr)

    stdscr.addstr(2,2,"What ticker would you like to retrieve")
    
    lantern_input = curses.newwin(5,30,4,2)
    rectangle(stdscr,1,0,7,32)
    stdscr.refresh()

    box = Textbox(lantern_input)
    box.edit()
    ticker = box.gather()

    return(ticker)

def main(stdscr):

    # Turn off Cursor blinking
    #    curses.curs_set(0)

    # Color Scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #type: ignore

    # specify the current selected row
    current_row = 0

    # Print the menu
    print_menu_main(stdscr, current_row)

    # Print the border
    print_border(stdscr)

    while 1:
        key = stdscr.getch()

        # Scrolling the page
        if key == curses.KEY_UP and current_row > 0: #type: ignore
            current_row -= 1 
        elif key == curses.KEY_DOWN and current_row < len(menu)-1: #type: ignore
            current_row += 1

        # Program Selection
        elif key == curses.KEY_ENTER or key in [10,13]: #type: ignore
         
            # If on last row: break
            if current_row == len(menu)-1:
                break
            
            #HACK: Gonna hardcode menu items to rownum
            if current_row == 0:
                ticker = print_menu_lantern(stdscr)
                stdscr.addstr(3,3,ticker)
                illuminate(ticker)
                stdscr.getch()
                
        # Else, go on
        print_menu_main(stdscr, current_row)
        print_border(stdscr)

curses.wrapper(main) #type: ignore





































    
