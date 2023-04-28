"""
test docstring
"""

import curses

__projectname__ = "Project Terminal"
__projectversion__ = "1.0"

menu = ['Home', 'Play', 'Scoreboard', 'Exit']

def print_border(stdscr):
    # Draw borders
    curses.curs_set(0) #type: ignore
    sh, sw = stdscr.getmaxyx()
     
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
    stdscr.addstr(0,2, f" {__projectname__} v{__projectversion__} ")
    stdscr.attroff(curses.color_pair(5)) #type: ignore
    stdscr.refresh()



def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    print_border(stdscr)
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
    	x = w//2 - len(row)//2
    	y = h//2 - len(menu)//2 + idx
    	if idx == selected_row_idx:
    		stdscr.attron(curses.color_pair(1))
    		stdscr.addstr(y, x, row)
    		stdscr.attroff(curses.color_pair(1))
    	else:
    		stdscr.addstr(y, x, row)
    stdscr.refresh()


def print_center(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y, x, text)
    stdscr.refresh()


def main(stdscr):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # specify the current selected row
    current_row = 0

    # print the menu
    print_menu(stdscr, current_row)

    # print the border
    print_border(stdscr)


    while 1:
    	key = stdscr.getch()

    	if key == curses.KEY_UP and current_row > 0:
    		current_row -= 1
    	elif key == curses.KEY_DOWN and current_row < len(menu)-1:
    		current_row += 1
    	elif key == curses.KEY_ENTER or key in [10, 13]:
    		print_center(stdscr, "You selected '{}'".format(menu[current_row]))
            stdscr.getch()
    		# if user selected last row, exit the program
    		if current_row == len(menu)-1:
                break

        print_menu(stdscr, current_row)
        print_border(stdscr)

curses.wrapper(main)









# Variables
# startx = 0
# starty = 0
#
# # Subwindow dimensions
# main_win_shiftx = 4
# main_win_shifty = 2
#  
#
#
# def main(stdscr):
#
#     # Draw borders
#     curses.curs_set(0) #type: ignore
#     sh, sw = stdscr.getmaxyx()
#     
#     border_y = sh-1
#     border_x = sw-2
#
#     for i in range (startx+1, border_y):
#          stdscr.addstr(i, startx, "│")
#          stdscr.addstr(i, border_x, "│")
#
#     # Horizontal Borders
#     for i in range (startx + 1, border_x):
#         stdscr.addstr(starty, i, "─")
#         stdscr.addstr(border_y, i, "─")
#
#     # Corners
#     stdscr.addstr(starty, startx, "╭")
#     stdscr.addstr(starty, border_x, "╮")
#     stdscr.addstr(border_y, startx, "╰")
#     stdscr.addstr(border_y, border_x, "╯")
#
#     # Title
#     stdscr.attron(curses.color_pair(5)) #type: ignore
#     stdscr.addstr(starty,border_x, f" {__projectname__} v{__projectversion__}")
#     stdscr.attroff(curses.color_pair(5)) #type: ignore
#
#
# curses.wrapper(main) #type: ignore
# #
#     # Title
#         # Attributes on, color = orange
#     stdscr.attron(curses.color_pair(5))  # type: ignore
#
#     stdscr.addstr(starty,startx+2, f" {__projectname__} v{__projectversion__} ")
#     stdscr.attroff(curses.color_pair(5)) # type: ignore
#
#     colors.init_colors()
#
#     # Bottom text instructions
#     tab = '    '
#     stdscr.addstr(endy+1,0, f"[Q] - Exit {tab} [H] - More Information")
#
#     stdscr.refresh()
#
#
#
# def draw_info_screen(stdscr):
#
#     endy, endx = stdscr.getmaxyx()
#     endx -= 1
#     endy -= 2
#     
#     info_screen = curses.newwin( # type: ignore
#
#     endy-starty-main_win_shifty, # Height
#     endx-startx-main_win_shiftx, # Width
#     starty+main_win_shifty, # Starting Y
#     startx+main_win_shiftx  # Starting X
#     )
#
#     info_screen.clear()
#     info_screen.addstr(0,0, lantern.__doc__)
#     info_screen.refresh()
#
# def draw_home_screen(stdscr):
#
#     endy, endx = stdscr.getmaxyx()
#     endx -= 1
#     endy -= 2
#
#     home_screen = curses.newwin( # type: ignore
#
#     endy-starty-main_win_shifty, # Height
#     endx-startx-main_win_shiftx, # Width
#     starty+main_win_shifty, # Starting Y
#     startx+main_win_shiftx  # Starting X
#     )
#
#     # Welcome message
#     home_screen.addstr(0,0, "Welcome to the Terminal")
#     home_screen.addstr(1,0, "Which software package would you like to run?")
#
#     # Terra Modules
#     home_screen.attron(curses.color_pair(5)) # type: ignore
#     home_screen.addstr(3,0, "Project Terra")
#     home_screen.attroff(curses.color_pair(5)) # type: ignore
#     home_screen.addstr(4,0, "Terra Nova")
#     home_screen.addstr(5,0, "Prima Terra")
#     home_screen.addstr(6,0, "Terra Erdos")
#
#     # Lantern Modules
#     home_screen.attron(curses.color_pair(5)) # type: ignore
#     home_screen.addstr(8,0, "Project Lantern")
#     home_screen.attroff(curses.color_pair(5)) # type: ignore
#
#     home_screen.addstr(9,0, "Illuminate")
#
#     # Eidos Modules
#     home_screen.attron(curses.color_pair(5)) # type: ignore
#
#     home_screen.addstr(11,0, "Project Eidos")
#     home_screen.attroff(curses.color_pair(5)) # type: ignore
#
#     home_screen.addstr(12,0, "Eidos Ranker")
#
#     # Initialize Cursor
#     home_screen.move(14,0)
#     home_screen.refresh()
#
# #def draw_lantern_screen():
#
#
# # FIX: I broke this whole thing mb
# def main(stdscr):
#     """ This will be the main app"""
#
#     stdscr.clear()
#
#     # Subwindow dimensions
#
#
#     draw_borders(stdscr)
#     # #------------------#
#     # #       UI         #
#     # #------------------#
#
#     # # Draw Borders
#
#     #     # Vertical Borders
#     # for i in range(starty + 1, endy):
#     #     stdscr.addstr(i, startx, "│")
#     #     stdscr.addstr(i, endx, "│")
#
#     #     # Horizontal Borders
#     # for i in range (startx + 1, endx):
#     #     stdscr.addstr(starty, i, "─")
#     #     stdscr.addstr(endy, i, "─")
#
#     #     # Corners
#     # stdscr.addstr(starty, startx, "╭")
#     # stdscr.addstr(starty, endx, "╮")
#     # stdscr.addstr(endy, startx, "╰")
#     # stdscr.addstr(endy, endx, "╯")
#
#     # # Title
#     #     # Attributes on, color = orange
#     # stdscr.attron(curses.color_pair(5))
#     # stdscr.addstr(starty,startx+2, f" {__projectname__} v{__projectversion__} ")
#     # stdscr.attroff(curses.color_pair(5))
#     # colors.init_colors()
#
#     # # Bottom text instructions
#     # tab = '    '
#     # stdscr.addstr(endy+1,0, f"[Q] - Exit {tab} [H] - More Information")
#
#     # stdscr.refresh()
#
#
#
#     # Window 1
#     # Welcome: Select your desired program
#     # window_num = 1
#
#     # home_screen = curses.newwin(
#     # endy-starty-main_win_shifty, # Height
#     # endx-startx-main_win_shiftx, # Width
#     # starty+main_win_shifty, # Starting Y
#     # startx+main_win_shiftx  # Starting X
#     # )
#
#     # # Welcome message
#     # home_screen.addstr(0,0, "Welcome to the Terminal")
#     # home_screen.addstr(1,0, "Which software package would you like to run?")
#
#     # # Terra Modules
#     # home_screen.attron(curses.color_pair(5))
#     # home_screen.addstr(3,0, "Project Terra")
#     # home_screen.attroff(curses.color_pair(5))
#     # home_screen.addstr(4,0, "Terra Nova")
#     # home_screen.addstr(5,0, "Prima Terra")
#     # home_screen.addstr(6,0, "Terra Erdos")
#
#     # # Lantern Modules
#     # home_screen.attron(curses.color_pair(5))
#     # home_screen.addstr(8,0, "Project Lantern")
#     # home_screen.attroff(curses.color_pair(5))
#     # home_screen.addstr(9,0, "Illuminate")
#
#     # # Eidos Modules
#     # home_screen.attron(curses.color_pair(5))
#     # home_screen.addstr(11,0, "Project Eidos")
#     # home_screen.attroff(curses.color_pair(5))
#     # home_screen.addstr(12,0, "Eidos Ranker")
#
#     # # Initialize Cursor
#     # home_screen.move(14,0)
#     # home_screen.refresh()
#
#     while 1:
#         draw_home_screen(stdscr)
#         key = home_screen.getch()
#         home_screen.clear()
#         # Quit
#         if key == ord("q"):
#             break
#
#         # Home
#         if key == ord("h"):
#             stdscr.clear()
#
#
#         # Info Screen
#         elif key == ord("i"):
#             draw_info_screen()
#
#
#
# curses.wrapper(main) # type: ignore
#
#
