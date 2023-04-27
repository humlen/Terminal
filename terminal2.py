import curses # pylint: disable=import-error
from src import colors,lantern

__projectname__ = "Project Terminal"
__projectversion__ = "1.0"

# Variables
startx = 0
starty = 0

# Subwindow dimensions
main_win_shiftx = 4
main_win_shifty = 2
 

def draw_borders(stdscr):
    """Draw the borders of the terminal"""
    
    endy, endx = stdscr.getmaxyx()
    endx -= 1
    endy -= 2
    # Draw Borders

        # Vertical Borders
    for i in range(starty + 1, endy):
        stdscr.addstr(i, startx, "│")
        stdscr.addstr(i, endx, "│")

        # Horizontal Borders
    for i in range (startx + 1, endx):
        stdscr.addstr(starty, i, "─")
        stdscr.addstr(endy, i, "─")

        # Corners
    stdscr.addstr(starty, startx, "╭")
    stdscr.addstr(starty, endx, "╮")
    stdscr.addstr(endy, startx, "╰")
    stdscr.addstr(endy, endx, "╯")

    # Title
        # Attributes on, color = orange
    stdscr.attron(curses.color_pair(5))  # type: ignore

    stdscr.addstr(starty,startx+2, f" {__projectname__} v{__projectversion__} ")
    stdscr.attroff(curses.color_pair(5)) # type: ignore

    colors.init_colors()

    # Bottom text instructions
    tab = '    '
    stdscr.addstr(endy+1,0, f"[Q] - Exit {tab} [H] - More Information")

    stdscr.refresh()



def draw_info_screen(stdscr):

    endy, endx = stdscr.getmaxyx()
    endx -= 1
    endy -= 2
    
    info_screen = curses.newwin( # type: ignore

    endy-starty-main_win_shifty, # Height
    endx-startx-main_win_shiftx, # Width
    starty+main_win_shifty, # Starting Y
    startx+main_win_shiftx  # Starting X
    )

    info_screen.clear()
    info_screen.addstr(0,0, lantern.__doc__)
    info_screen.refresh()

def draw_home_screen(stdscr):

    endy, endx = stdscr.getmaxyx()
    endx -= 1
    endy -= 2

    home_screen = curses.newwin( # type: ignore

    endy-starty-main_win_shifty, # Height
    endx-startx-main_win_shiftx, # Width
    starty+main_win_shifty, # Starting Y
    startx+main_win_shiftx  # Starting X
    )

    # Welcome message
    home_screen.addstr(0,0, "Welcome to the Terminal")
    home_screen.addstr(1,0, "Which software package would you like to run?")

    # Terra Modules
    home_screen.attron(curses.color_pair(5)) # type: ignore
    home_screen.addstr(3,0, "Project Terra")
    home_screen.attroff(curses.color_pair(5)) # type: ignore
    home_screen.addstr(4,0, "Terra Nova")
    home_screen.addstr(5,0, "Prima Terra")
    home_screen.addstr(6,0, "Terra Erdos")

    # Lantern Modules
    home_screen.attron(curses.color_pair(5)) # type: ignore
    home_screen.addstr(8,0, "Project Lantern")
    home_screen.attroff(curses.color_pair(5)) # type: ignore

    home_screen.addstr(9,0, "Illuminate")

    # Eidos Modules
    home_screen.attron(curses.color_pair(5)) # type: ignore

    home_screen.addstr(11,0, "Project Eidos")
    home_screen.attroff(curses.color_pair(5)) # type: ignore

    home_screen.addstr(12,0, "Eidos Ranker")

    # Initialize Cursor
    home_screen.move(14,0)
    home_screen.refresh()

#def draw_lantern_screen():


# FIX: I broke this whole thing mb
def main(stdscr):
    """ This will be the main app"""

    stdscr.clear()

    # Subwindow dimensions


    draw_borders(stdscr)
    # #------------------#
    # #       UI         #
    # #------------------#

    # # Draw Borders

    #     # Vertical Borders
    # for i in range(starty + 1, endy):
    #     stdscr.addstr(i, startx, "│")
    #     stdscr.addstr(i, endx, "│")

    #     # Horizontal Borders
    # for i in range (startx + 1, endx):
    #     stdscr.addstr(starty, i, "─")
    #     stdscr.addstr(endy, i, "─")

    #     # Corners
    # stdscr.addstr(starty, startx, "╭")
    # stdscr.addstr(starty, endx, "╮")
    # stdscr.addstr(endy, startx, "╰")
    # stdscr.addstr(endy, endx, "╯")

    # # Title
    #     # Attributes on, color = orange
    # stdscr.attron(curses.color_pair(5))
    # stdscr.addstr(starty,startx+2, f" {__projectname__} v{__projectversion__} ")
    # stdscr.attroff(curses.color_pair(5))
    # colors.init_colors()

    # # Bottom text instructions
    # tab = '    '
    # stdscr.addstr(endy+1,0, f"[Q] - Exit {tab} [H] - More Information")

    # stdscr.refresh()



    # Window 1
    # Welcome: Select your desired program
    # window_num = 1

    # home_screen = curses.newwin(
    # endy-starty-main_win_shifty, # Height
    # endx-startx-main_win_shiftx, # Width
    # starty+main_win_shifty, # Starting Y
    # startx+main_win_shiftx  # Starting X
    # )

    # # Welcome message
    # home_screen.addstr(0,0, "Welcome to the Terminal")
    # home_screen.addstr(1,0, "Which software package would you like to run?")

    # # Terra Modules
    # home_screen.attron(curses.color_pair(5))
    # home_screen.addstr(3,0, "Project Terra")
    # home_screen.attroff(curses.color_pair(5))
    # home_screen.addstr(4,0, "Terra Nova")
    # home_screen.addstr(5,0, "Prima Terra")
    # home_screen.addstr(6,0, "Terra Erdos")

    # # Lantern Modules
    # home_screen.attron(curses.color_pair(5))
    # home_screen.addstr(8,0, "Project Lantern")
    # home_screen.attroff(curses.color_pair(5))
    # home_screen.addstr(9,0, "Illuminate")

    # # Eidos Modules
    # home_screen.attron(curses.color_pair(5))
    # home_screen.addstr(11,0, "Project Eidos")
    # home_screen.attroff(curses.color_pair(5))
    # home_screen.addstr(12,0, "Eidos Ranker")

    # # Initialize Cursor
    # home_screen.move(14,0)
    # home_screen.refresh()

    while 1:
        draw_home_screen(stdscr)
        key = home_screen.getch()
        home_screen.clear()
        # Quit
        if key == ord("q"):
            break

        # Home
        if key == ord("h"):
            stdscr.clear()


        # Info Screen
        elif key == ord("i"):
            draw_info_screen()



curses.wrapper(main) # type: ignore


