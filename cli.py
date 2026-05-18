import os
import sys
import json
import curses
import shutil
import constants as c
import utils as Utils
from configs import cut_config

COLORS = {
    # SELECTED
    # DESELECTED
    # INACTIVE
    # ACTIVE
    # LABEL
}

def init_colors(stdscr):
    combos = [ #(F,B)
    ("SELECTED", curses.COLOR_WHITE,curses.COLOR_RED),
    ("DESELECTED", curses.COLOR_YELLOW,curses.COLOR_BLACK),
    ("INACTIVE", curses.COLOR_WHITE, curses.COLOR_BLACK),
    ("ACTIVE", curses.COLOR_BLACK, curses.COLOR_WHITE),
    ("LABEL", curses.COLOR_BLUE, curses.COLOR_BLACK)]
    curses.start_color()
    curses.use_default_colors()

    for i, (name, fg, bg) in enumerate(combos, start=1):
        curses.init_pair(i, fg, bg)
        COLORS[name] = curses.color_pair(i)

def print_preset_options(stdscr, tmargin: int, lmargin: int, is_active: bool):
    """Input: (stdscr, tmargin: int, lmargin: int, is_active: bool)
    Output: tmargin: the new margin to begin printing from after these preset"""
    preset_config = cut_config.get_presets()
    # print label
    if len(preset_config["l"]) > 0:
        stdscr.addstr(tmargin, lmargin, preset_config["l"])
        tmargin += 1
    # print presets
    preset_index = cut_config.get_current_preset_index()
    for i, j in enumerate(preset_config["p"]):
        if i == 0:
            stdscr.move(tmargin, lmargin)
        if i == preset_index:
            stdscr.addstr(f"< {j["n"]} >", COLORS["SELECTED"])
        else:
            if is_active:
                stdscr.addstr(f"  {j["n"]}  ", COLORS["ACTIVE"])
            else:
                stdscr.addstr(f"  {j["n"]}  ", COLORS["DESELECTED"])
    if preset_index == -1:
        stdscr.addstr(" < Custom > ", COLORS["SELECTED"])
    # return the new top margin after printing all of this
    return tmargin + 1

def print_menu_options(stdscr, tmargin: int, lmargin: int, current_index: int):
    menu_len = cut_config.get_menu_length()
    for i in range(menu_len):
        menu_option = cut_config.get_menu_option_by_index(i)

        # if there is a label, print it
        if len(menu_option["l"]) > 0:
            stdscr.addstr(i+tmargin, lmargin, menu_option["l"], COLORS["LABEL"])
            tmargin += 1 # assumes that the label is a one-liner

        # print selectables
        q_string = f"{menu_option["q"]} "
        if i == current_index:
            stdscr.addstr(i+tmargin, lmargin, q_string, COLORS["ACTIVE"])
        else:
            stdscr.addstr(i+tmargin, lmargin, q_string, COLORS["INACTIVE"])
        for j, o in enumerate(menu_option["a"]):
            if j == 0:
                stdscr.move(i+tmargin, lmargin + len(q_string))
            if cut_config.get_state_by_index(i) == j:
                stdscr.addstr(f" {o} ", COLORS["SELECTED"])
            else:
                stdscr.addstr(f" {o} ", COLORS["DESELECTED"])

def handle_keypress(stdscr, current_index):
    """handles arrow keys and returns the updated index. -1 through len(menu)-1
    if the user confirms their choice, return None"""
    key = stdscr.getch()

    # Navigation
    if key in [curses.KEY_UP, 450]:
        # allow the index to reach -1 for selecting presets
        if current_index > -1:
            return current_index - 1
    elif key in [curses.KEY_DOWN, 456]:
        if current_index < cut_config.get_menu_length()-1:
            return current_index + 1
    elif key in [curses.KEY_LEFT, 452]:
        cut_config.set_decrement_option_by_index(current_index)
        return current_index
    elif key in [curses.KEY_RIGHT, 454]:
        cut_config.set_increment_option_by_index(current_index)
        return current_index
    elif key in [curses.KEY_ENTER,10,32]:  # Space/Enter key confirms selection
        return None

def confirm_choices(stdscr):
    stdscr.clear()
    longest = cut_config.get_longest_question_len()
    row = 4
    stdscr.addstr(2, 2, "Your selections:", curses.A_BOLD)

    for i in range(cut_config.get_menu_length()):
        option = cut_config.get_menu_option_by_index(i)
        question = option["q"]
        state = cut_config.get_state_by_index(i)
        stdscr.addstr(i+4, 2, f"{question:>{longest}} - {option["a"][state]}")
        row += 1
    stdscr.addstr(row+1, 2, "Press SPACE/ENTER to confirm or any other key to exit")

    stdscr.refresh()
    key = stdscr.getch()

    if key in [curses.KEY_ENTER,10,32]:  # Enter key confirms selection
        return
    else:
        return -1

def set_cutmap_options():
    """main CLI function for selecting cut options
    returns: -1 if user did not confirm choices"""
    def menu(stdscr):
        stdscr.keypad(True)
        curses.curs_set(0)
        init_colors(stdscr)
        current_index = 0  # Current menu position
        margin_l = 2

        while True:
            stdscr.clear()

            # Instructions
            inst = [
                "= = = CHOOSE YOUR 35PC CUT PARAMETERS - HOW MUCH FILLER TO CUT? = = =",
                "Use ↑/↓ to navigate, ←/→ to set an option, SPACE/ENTER to confirm",
                ""
            ]
            margin_t = len(inst)

            for i, line in enumerate(inst):
                stdscr.addstr(i, margin_l, line)

            margin_t = print_preset_options(stdscr, margin_t, margin_l, current_index == -1)
            print_menu_options(stdscr, margin_t, margin_l, current_index)
            current_index = handle_keypress(stdscr, current_index)
            if current_index is None:
                Utils.log("VERBOSE: User confirmed choices. Exiting CLI.")
                break
            stdscr.refresh()

        return confirm_choices(stdscr)
    return curses.wrapper(menu)