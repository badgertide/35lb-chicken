"""This gets a little complex and I want it to be
    as useable as possible.
    l: Label
    p: Preset
        n: Preset Name
        o: Preset Options
        t: Alt Text
    q: Query
        a: Answers"""

import utils as Utils
import constants as c

class _CutConfig:
    """Holds and manages the CLI menu"""
    _instance = None

    def __init__(self):
        self.presets = {
            "l": "= Preset Cuts (Enter to set) =",
            "p": [
                {"n": "Minimal", "o": [0,0,0,0,0,0,0,0,0,0,0], "t": "Single episodes, only cut filler"},
                {"n": "Default", "o": [1,1,1,0,1,1,1,2,1,4,0], "t": "5-episode runs, cut titles, teasers, tbc, keep one eyecatcher"},
                {"n": "Maximum", "o": [2,2,2,1,2,2,2,2,2,0,0], "t": "One run, cut as much as possible (some episodes end in strange places)"}
                ]
            }
        self.menu = [
            {
                "l": "= Episode Start Options =",
                "q": "Production Logos",
                "k": "production",
                "a": ["Keep", "On Run Start", "Cut"]
            },
            {
                "l": "",
                "q": "Opening Themes",
                "k": "themeopen",
                "a": ["Keep", "On Run Start", "Cut"]
            },
            {
                "l": "",
                "q": "Recap",
                "k": "recap",
                "a": ["Keep", "On Run Start", "Cut"]
            },
            {
                "l": "= Mid-episode Options =",
                "q": "Title Cards",
                "k": "titlecard",
                "a": ["Keep", "Cut"]
            },
            {
                "l": "",
                "q": "Bumpers/Eyecatchers",
                "k": "eyecatcher",
                "a": ["Keep All", "Keep First", "Cut"]
            },
            {
                "l": "= Episode End Options =",
                "q": "To Be Continued",
                "k": "tbc",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Closing Themes",
                "k": "themeclose",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Teasers",
                "k": "teaser",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Signoff Panes",
                "k": "signoff",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "= Other Options =",
                "q": "Episodes Per Run",
                "k": "",
                "a": [1, 2, 3, 4, 5]
            },
            {
                "l": "1: Scenes, 2: Episodes (Except G-8), 3: All Non-Canon Content",
                "q": "Filler Pool",
                "k": "",
                "a": [1]
            }
        ]
        self.state = [1,1,1,0,1,1,1,2,1,4,0]
        self._validate()

    def _validate(self):
        internal_presets = self.presets["p"]
        found_error = False
        for c in internal_presets:
            c_error = False
            # check that each config has the same number of options as the menu offers
            if len(c["o"]) != len(self.menu):
                Utils.log(f"ERROR: CutConfig - Preset [{c["n"]}] is length [{len(c["o"])}], should be [{len(self.menu)}]")
                found_error = True
                c_error = True
            for j, o in enumerate(c["o"]):
                # for the current config, check that all preset options exist
                if not c_error and not 0 <= o < len(self.menu[j]["a"]):
                    Utils.log(f"ERROR: CutConfig - Preset [{c["n"]}] has invalid selection [{o}] for option [{j}]")
                    found_error = True
        if found_error:
            raise IndexError
        # Check that every option has a label
        if "l" not in self.presets:
            Utils.log("ERROR: CutConfig - Config is lacking a label")
            found_error = True
        for i, o in enumerate(self.menu):
            if not "l" in o:
                Utils.log(f"ERROR: CutConfig - Menu option [{i}] is lacking a label")
                found_error = True
            if o["q"] in ["Episodes Per Run", "Filler Pool"]:
                if not all([isinstance(x, (int)) for x in o["a"]]):
                    Utils.log(f"ERROR: CutConfig - Integer menu option [{i}] is not entirely integers")
                    found_error = True
        if found_error:
            raise ValueError


    def __new__(cls):
        # enforce singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # Getters ==========

    def get_presets(self):
        return self.presets

    def get_preset_options_by_index(self, i: int):
        if 0 <= i <len(self.presets["p"]):
            return self.presets["p"][i]
        else:
            raise IndexError

    def get_menu_length(self):
        return len(self.menu)

    def get_menu_option_by_index(self, i: int):
        if 0 <= i <len(self.menu):
            return self.menu[i]
        else:
            raise IndexError

    def get_menu_option_length_by_index(self, i):
        if 0 <= i <len(self.menu):
            return len(self.menu[i]["a"])
        else:
            raise IndexError
    
    def get_longest_question_len(self):
        longest = max(self.menu, key=lambda x: len(x["q"]))["q"]
        return len(longest)

    def get_state(self):
        return self.state

    def get_state_by_index(self, i: int):
        if i>=0 and i<len(self.state):
            return self.state[i]
        else:
            raise IndexError
    
    def get_current_preset_index(self):
        """if state is [0,0,0]
        and presets are [2,2,2], [1,1,1], and [0,0,0],
        return 2 to indicate that 2 is the currently active preset"""
        for i, p in enumerate(self.presets["p"]):
            if self.state == p["o"]:
                return i
        return -1

    def get_selected_fillers(self):
        # TODO this should return the filler that the user wants to cut
        return c.FILLER_TYPES

    def get_option_cats(self):
        """Used for getting the currently stored settings
        Returns: a dict with properties
        run_len: the number of episodes in a run
        filler: the filler pool that will be cut - "filler_1"
        keep: this segment should render under all curcumstances
        keep_first: this segment should render ONLY if this is the first episode in a run
        keep_last: this segment should render ONLY if this is the last episode in a run
        keep_one: if there are multiples of this segment in an episode, render only one (for now, this is the first one)
        drop: do not render this segment under any circumstances"""
        cats = {
            "run_len": 0,
            "filler": 0,
            "keep": ["generic"],
            "keep_first": [],
            "keep_last": ["easeout"],
            "keep_one": [],
            "drop": [],
        }
        for i in range(self.get_menu_length()):
            option = self.get_menu_option_by_index(i)
            question = option["q"]
            answers = option["a"]
            key = option["k"]
            state = self.get_state_by_index(i)

            if question == "Episodes Per Run":
                cats["run_len"] = answers[state]
                break
            if question == "Filler Pool":
                cats["filler"] = answers[state]
                break

            match answers[state]:
                case "Keep":
                    cats["keep"].append(key)
                case "On Run Start":
                    cats["keep_first"].append(key)
                case "On Run End":
                    cats["keep_last"].append(key)
                case "Keep First":
                    cats["keep_one"].append(key)
                case "Cut":
                    cats["drop"].append(key)
                case _:
                    Utils.log(f"ERROR: Option [{question}] has an unknown selection [{answers[state]}]")
        return cats


    # Setters ==========

    def set_selection(self, i: int, selection: int):
        """Input: (1,2)
           State: [3,4,5]
           Sets 4 -> 2 if this is a valid choice"""
        if i>=0 and i<len(self.state) and selection>=0 and selection<len(self.menu[i]["a"]):
            self.state[i] = selection
        else:
            Utils.log(f"ERROR: CutConfig set_selection({i}, {selection}) is out of range")
            raise IndexError

    def set_state_to_preset(self, i: int):
        if not 0 <= i <len(self.presets["p"]):
            raise IndexError
        else:
            self.state = list(self.presets["p"][i]["o"])

    def set_increment_option_by_index(self, i:int):
        """increment the selected option by 1
        if this is not possible, do nothing"""
        if i == -1:
            # special case for selecting presets
            self._increment_preset(i)
            return
        if not 0 <= i <len(self.menu):
            raise IndexError
        current = self.get_state_by_index(i)
        length = len(self.menu[i]["a"])
        if current < length - 1:
            self.set_selection(i, current + 1)

    def set_decrement_option_by_index(self, i:int):
        """decrement the selected option by 1
        if this is not possible, do nothing"""
        if i == -1:
            # special case for selecting presets
            self._decrement_preset(i)
            return
        if not 0 <= i <len(self.menu):
            raise IndexError
        current = self.get_state_by_index(i)
        if current > 0:
            self.set_selection(i, current - 1)
    
    # Presets ==========
    # Presets don't have an integer to track which one is selected
    # since they select and deselect as the user marks options
    # Presets: [0,1,2], -1 == Custom

    def _increment_preset(self, i):
        # get the currently used preset
        current_index = self.get_current_preset_index()
        length = len(self.presets["p"])
        # if no preset, do nothing
        if current_index == -1:
            return
        elif current_index >= length-1:
            return
        else:
            self.set_state_to_preset(current_index+1)
        

    def _decrement_preset(self, i):
        # get the currently used preset
        current_index = self.get_current_preset_index()
        length = len(self.presets["p"])
        # if no preset, set to the last preset
        if current_index == -1:
            self.set_state_to_preset(length-1)
        elif current_index <= 0:
            return
        else:
            self.set_state_to_preset(current_index-1)

cut_config = _CutConfig()
