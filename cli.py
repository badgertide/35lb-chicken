import os
import sys
import json
import curses
import shutil
import constants as c
import utils as Utils

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

def get_cutmap_options():
    options = c.CUT_OPTIONS_MENU
    def get_option_from_index(i):
        """the cut menu and the actual options don't match up due to the labels
        Translate the absolute index to the nth option (ex. 7 -> 4)"""
        if options[i]["type"] == "l":
            return None
        return sum(1 for x in options[:i+1] if not x["type"] == "l") - 1

    def menu(stdscr):
        stdscr.keypad(True)
        curses.curs_set(0)
        init_colors(stdscr)
        # although the options array has 17 elements, there are only 11 valid options
        selections = [0] * len([x for x in options if not x["type"] == "l"])  # Track selections
        current_index = 1  # Current menu position

        while True:
            stdscr.clear()

            # Instructions
            inst = [
                "= = = CHOOSE YOUR 35PC CUT PARAMETERS - HOW MUCH FILLER TO CUT? = = =",
                "Use ↑/↓ to navigate, ←/→ to set an option, SPACE/ENTER to confirm",
                ""
            ]
            margin_t = len(inst)
            margin_l = 2
            max_height, max_width = stdscr.getmaxyx()


            for i, line in enumerate(inst):
                stdscr.addstr(i, margin_l, line)

            # add line from all elements
            for i, e in enumerate(options):
                if e["type"] == "l":
                    label = e["l"]
                    stdscr.addstr(i+margin_t, margin_l, label, COLORS["LABEL"])
                elif e["type"] == "q":
                    q_string = f"{e["q"]} "
                    if i == current_index:
                        stdscr.addstr(i+margin_t, margin_l, q_string, COLORS["ACTIVE"])
                    else:
                        stdscr.addstr(i+margin_t, margin_l, q_string, COLORS["INACTIVE"])
                    for i2, j in enumerate(e["a"]):
                        if i2 == 0:
                            stdscr.move(i+margin_t, margin_l + len(q_string))
                        if selections[get_option_from_index(i)] == i2:
                            stdscr.addstr(f" {j} ", COLORS["SELECTED"])
                        else:
                            stdscr.addstr(f" {j} ", COLORS["DESELECTED"])
                elif e["type"] == "c":
                    is_custom = True
                    for i2, j in enumerate(e["c"]):
                        if i2 == 0:
                            stdscr.move(i+margin_t, margin_l)
                        # if the 1+ indices of the array match, then j is our current config
                        if selections[1:] == j["o"]:
                            stdscr.addstr(f" < {j["n"]} > ", COLORS["SELECTED"])
                            is_custom = False
                        elif not selections[1:] == j["o"] and i == current_index:
                            stdscr.addstr(f" < {j["n"]} > ", COLORS["ACTIVE"])
                        else:
                            stdscr.addstr(f" < {j["n"]} > ", COLORS["DESELECTED"])
                    if is_custom:
                        stdscr.addstr(" < Custom > ", COLORS["SELECTED"])
                        selections[get_option_from_index(i)] = len(e["c"])
                    elif not is_custom and i == current_index:
                        stdscr.addstr(" < Custom > ", COLORS["ACTIVE"])
                    else:
                        stdscr.addstr(" < Custom > ", COLORS["DESELECTED"])
            stdscr.refresh()
            # Wait for character
            key = stdscr.getch()
            option_index = get_option_from_index(current_index)

            # Navigation
            if key in [curses.KEY_UP, 450]:
                # Navigate up to the prev non-label, no loop
                if current_index > 0:
                    nextup = current_index - 1
                    while nextup > 0 and options[nextup]["type"] == "l":
                        nextup -= 1
                    if nextup > 0:
                        current_index = nextup

            elif key in [curses.KEY_DOWN, 456]:
                # Navigate down to the next non-label, no loop
                if current_index < len(options)-1:
                    nextup = current_index + 1
                    while nextup < len(options)-1 and options[nextup]["type"] == "l":
                        nextup += 1
                    current_index = nextup

            elif key in [curses.KEY_LEFT, 452]:
                if options[current_index]["type"] == "l":
                    Utils.print_to_log(f"WARN: index {current_index} is a label")
                elif options[current_index]["type"] == "q":
                    if selections[option_index] > 0:
                        selections[option_index] -= 1
                elif options[current_index]["type"] == "c":
                    current_preset = selections[option_index]
                    all_presets = options[current_index]["c"]
                    if current_preset > 0:
                        selections[option_index] -= 1
                        current_preset = selections[option_index]
                        selections = selections[:1] + all_presets[current_preset]["o"]

            elif key in [curses.KEY_RIGHT, 454]:
                if options[current_index]["type"] == "l":
                    Utils.print_to_log(f"WARN: index {current_index} is a label")
                elif options[current_index]["type"] == "q":
                    option_index = get_option_from_index(current_index)
                    if selections[option_index] < len(options[current_index]["a"])-1:
                        selections[option_index] += 1
                elif options[current_index]["type"] == "c":
                    current_preset = selections[option_index]
                    all_presets = options[current_index]["c"]
                    if selections[option_index] < len(all_presets)-1:
                        selections[option_index] += 1
                        current_preset = selections[option_index]
                        selections = selections[:1] + all_presets[current_preset]["o"]
                stdscr.refresh()

            elif key in [32, 10]:  # Space/Enter key confirms selection
                break

        # Confirm Choices
        #################

        # stdscr.clear()
        # selectedOptions = [options[i] for i in range(len(options)) if selected[i]]
        # unselectedOptions = [options[i] for i in range(len(options)) if not selected[i]]
        # stdscr.addstr(2, 2, f"{'You selected '+str(len(selectedOptions))+'/'+str(len(options)):^50}", curses.A_BOLD)
        # stdscr.addstr(3, 2, f"{'Write '+str(len(selectedOptions))+' selected videos to batchURLs.txt':^50}")
        # stdscr.addstr(4, 2, f"{'and '+str(len(unselectedOptions))+' others to the archive':^50}")
        # stdscr.addstr(6, 2, "Press ENTER to confirm or any other key to go back")

        stdscr.refresh()
        key = stdscr.getch()  # Wait for key press

        if key in [32,10]:  # Enter key confirms selection
            return {}
    return curses.wrapper(menu)