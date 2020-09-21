import curses

menu = ['Home', 'Play', 'Scoreboard', 'Exit']
close_options = ['Yes', 'No']

def print_menu(stdscr, selected_row_idx):
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

def print_close_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()

    menu_text = 'Are you sure you want to quit?'
    stdscr.addstr(0, w//2 - len(menu_text)//2, menu_text)

    for idx, row in enumerate(close_options):
        x = w//2 - len(row)//2
        y = h//2 - len(close_options)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def close_menu_loop(stdscr, current_closing_menu_row_idx):
    running = True

    while True:
        print_close_menu(stdscr, current_closing_menu_row_idx)

        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_closing_menu_row_idx > 0:
            current_closing_menu_row_idx -= 1
        elif key == curses.KEY_DOWN and current_closing_menu_row_idx < len(close_options) - 1:
            current_closing_menu_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if close_options[current_closing_menu_row_idx] == 'Yes':
                running = False
            break

        print_close_menu(stdscr, current_closing_menu_row_idx)
        stdscr.refresh()
    return running

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0
    current_closing_menu_row_idx = 0
    running = True

    print_menu(stdscr, current_row_idx)
    
    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == 27: # ESC or ALT
            current_closing_menu_row_idx = 0
            if not close_menu_loop(stdscr, current_closing_menu_row_idx):
                running = False
        elif key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row_idx == len(menu) - 1:
                current_closing_menu_row_idx = 0
                if not close_menu_loop(stdscr, current_closing_menu_row_idx):
                    break
        
        if running:
            print_menu(stdscr,  current_row_idx)
            stdscr.refresh()
        else:
            break


curses.wrapper(main)