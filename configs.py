"""This gets a little complex and I want it to be
    as useable as possible.
    l: Label
    c: Config
        n: Config Name
        o: Preset Options
        t: Alt Text
    q: Query
        a: Answers"""

import utils as Utils

class CutConfig:
    """Holds and manages the CLI menu"""
    _instance = None

    def __init__(self):
        self.configs = {
            "l": "= Preset Cuts (Enter to set) =",
            "c": [
                {"n": "Minimal", "o": [0,0,0,0,0,0,0,0,0,0], "t": "Single episodes, only cut filler"},
                {"n": "Default", "o": [1,1,0,1,1,1,2,1,4,0], "t": "5-episode runs, cut titles, teasers, tbc, keep one eyecatcher"},
                {"n": "Maximum", "o": [2,2,1,2,2,2,2,2,0,0], "t": "One run, cut as much as possible (some episodes end in strange places)"}
                ]
            }
        self.menu = [
            {
                "l": "= Episode Start Options =",
                "q": "Production Logos",
                "a": ["Keep", "On Run Start", "Cut"]
            },
            {
                "l": "",
                "q": "Opening Themes",
                "a": ["Keep", "On Run Start", "Cut"]
            },
            {
                "l": "= Mid-episode Options =",
                "q": "Title Cards",
                "a": ["Keep", "Cut"]
            },
            {
                "l": "",
                "q": "Bumpers/Eyecatchers",
                "a": ["Keep All", "Keep First", "Cut"]
            },
            {
                "l": "= Episode End Options =",
                "q": "To Be Continued",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Closing Themes",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Teasers",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "",
                "q": "Signoff Panes",
                "a": ["Keep", "On Run End", "Cut"]
            },
            {
                "l": "= Other Options =",
                "q": "Episodes Per Run",
                "a": ["1", "2", "3", "4", "5"]
            },
            {
                "l": "1: Scenes, 2: Episodes (Except G-8), 3: All Non-Canon Content",
                "q": "Filler Pool",
                "a": ["1"]
            }
        ]
        self.state = [0] * len(self.menu)
        self._validate()

    def _validate(self):
        internal_configs = self.configs["c"]
        found_error = False
        for c in internal_configs:
            c_error = False
            # check that each config has the same number of options as the menu offers
            if len(c["o"]) != len(self.menu):
                Utils.log(f"ERROR: CutConfig preset [{c["n"]}] is length [{len(c["o"])}], should be [{len(self.menu)}]")
                found_error = True
                c_error = True
            for j, o in enumerate(c["o"]):
                # for the current config, check that all preset options exist 
                if not c_error and not 0 <= o < len(self.menu[j]["a"]):
                    Utils.log(f"ERROR: CutConfig preset [{c["n"]}] has invalid selection [{o}] for option [{j}]")
                    found_error = True
        if found_error:
            raise IndexError

    def __new__(cls):
        # enforce singleton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # Getters ==========

    def get_configs(self):
        return self.configs

    def get_menu_length(self):
        return len(self.menu)

    def get_menu_option_at_index(self, i: int):
        if i>=0 and i<len(self.menu):
            return self.menu[i]
        else:
            raise IndexError

    def get_state(self):
        return self.state

    def get_selection_at_index(self, i: int):
        if i>=0 and i<len(self.state):
            return self.state[i]
        else:
            raise IndexError

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
    # TODO more setters probably
