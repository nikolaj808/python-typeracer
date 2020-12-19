import curses

main_menu_options = ['Play', 'Stats', 'Exit']
close_menu_options = ['Yes', 'No']

def getch(stdscr):
    key = stdscr.getch()

    while (key == curses.ERR):
        key = stdscr.getch()
    return key

def get_correct_substring(player_text: str, text: str):
    index = 0
    player_text_length = len(player_text)
    text_length = len(text)

    if (player_text_length > 0):
        while index < player_text_length and index < text_length:
            if player_text[index] == text[index]:
                index += 1
            else:
                return player_text[0:index]
        return player_text[0:index]
    else:
        return ''

def print_main_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(main_menu_options):
        x = w//2 - len(row)//2
        y = h//2 - len(main_menu_options)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def print_play_menu(stdscr, typeracer_text, current_player_text):
    h, w = stdscr.getmaxyx()
    menu_title = 'Play Menu'
    typeracer_words = typeracer_text.split(' ')

    menu_title_y = h//8
    menu_title_x = w//2 - len(menu_title)//2
    
    typeracer_text_y = h//4

    stdscr.addstr(menu_title_y, menu_title_x, menu_title)



    correct = get_correct_substring(current_player_text, typeracer_text)
    correct_length = len(correct)
    false_length = len(current_player_text) - correct_length
    correct_and_false_length = correct_length + false_length
    unwritten_length = (len(typeracer_text) - correct_and_false_length) if len(typeracer_text) > correct_and_false_length else 0

    stdscr.addstr(typeracer_text_y, 0, typeracer_text[0:correct_length])
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(typeracer_text_y, correct_length, typeracer_text[correct_length:correct_and_false_length])
    stdscr.attroff(curses.color_pair(3))

    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(typeracer_text_y, correct_and_false_length, typeracer_text[correct_and_false_length:len(typeracer_text)])
    stdscr.attroff(curses.color_pair(2))

    stdscr.refresh()

def print_before_play_menu(stdscr):
    h, w = stdscr.getmaxyx()
    menu_title = 'Play Menu'
    typeracer_text = 'This is a test text to test the functionality'
    instruction_text = '^^ Type this text. Game starts when you press ENTER ^^'

    menu_title_y = h//8
    menu_title_x = w//2 - len(menu_title)//2
    
    typeracer_text_y = h//4
    instruction_text_y = h//2

    stdscr.addstr(menu_title_y, menu_title_x, menu_title)
    stdscr.addstr(typeracer_text_y, 0, typeracer_text)
    stdscr.addstr(instruction_text_y, 0, instruction_text)
    stdscr.refresh()

def play_menu_loop(stdscr):
    running = True
    typeracer_text = 'This is a test text to test the functionality'
    typeracer_words = typeracer_text.split(' ')
    word_index = 0
    player_text = ''

    print_before_play_menu(stdscr)

    key = getch(stdscr)

    stdscr.clear()

    while True:
        print_play_menu(stdscr, player_text, typeracer_words[word_index])

        key = getch(stdscr)

        stdscr.clear()

        if key == 27:
            break
        elif key == 8:
            player_text = player_text[0:len(player_text) - 1]
        else:
            player_text += chr(key)

def print_close_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()

    menu_text = 'Are you sure you want to quit?'
    stdscr.addstr(0, w//2 - len(menu_text)//2, menu_text)

    for idx, row in enumerate(close_menu_options):
        x = w//2 - len(row)//2
        y = h//2 - len(close_menu_options)//2 + idx
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
        elif key == curses.KEY_DOWN and current_closing_menu_row_idx < len(close_menu_options) - 1:
            current_closing_menu_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if close_menu_options[current_closing_menu_row_idx] == 'Yes':
                running = False
            break

        print_close_menu(stdscr, current_closing_menu_row_idx)
        stdscr.refresh()
    return running

def main(stdscr):
    curses.curs_set(0) # disable cursor visibility
    curses.use_default_colors()
    # curses.init_color(1, 71, 73, 72)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Currently selected item
    curses.init_pair(2, 8, curses.COLOR_BLACK) # Unwritten text
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    
    stdscr.nodelay(True)

    running = True
    current_main_menu_row_idx = 0
    current_closing_menu_row_idx = 0

    print_main_menu(stdscr, current_main_menu_row_idx)
    
    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == 27: # ESC or ALT
            current_closing_menu_row_idx = 0
            if not close_menu_loop(stdscr, current_closing_menu_row_idx):
                running = False
        elif key == curses.KEY_UP and current_main_menu_row_idx > 0:
            current_main_menu_row_idx -= 1
        elif key == curses.KEY_DOWN and current_main_menu_row_idx < len(main_menu_options) - 1:
            current_main_menu_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if main_menu_options[current_main_menu_row_idx] == 'Play':
                play_menu_loop(stdscr)
            elif main_menu_options[current_main_menu_row_idx] == 'Exit':
                current_closing_menu_row_idx = 0
                if not close_menu_loop(stdscr, current_closing_menu_row_idx):
                    break
        
        if running:
            print_main_menu(stdscr,  current_main_menu_row_idx)
            stdscr.refresh()
        else:
            break
    
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

curses.wrapper(main)