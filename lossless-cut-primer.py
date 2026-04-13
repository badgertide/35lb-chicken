import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

import utils as Utils

"""set the base template for each chunk of episodes
this can help save time if the theme song changes each season
or certain segments start/stop being utilized"""
TEMPLATES = {
    "OnePiece": [
        {
            "name": "East Blue",
            "startend": [1,62],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 779.9875416666666,
                "name": 'segment'
                },
                {
                "start": 779.9875416666666,
                "end": 786.9945416666666,
                "name": 'eyecatcher'
                },
                {
                "start": 786.9945416666666,
                "end": 794.5020416666666,
                "name": 'eyecatcher'
                },
                {
                "start": 794.5020416666666,
                "end": 1390.0136249999998,
                "name": 'segment'
                },
                {
                "start": 1390.0136249999998,
                "end": 1390.0136249999998,
                "name": 'easeout'
                },
                {
                "start": 1390.0136249999998,
                "end": 1460.0002083333331,
                "name": 'themeclose'
                },
                {
                "start": 1460.0002083333331,
                "end": 1489.9885,
                "name": 'teaser'
                },
                {
                "start": 1489.9885,
                "end": 1500.0302083333331,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "The Grand Line",
            "startend": [63,77],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.95816666666666,
                "name": 'themeopen'
                },
                {
                "start": 124.95816666666666,
                "end": 124.95816666666666,
                "name": 'easein'
                },
                {
                "start": 124.95816666666666,
                "end": 776.0252499999999,
                "name": 'segment'
                },
                {
                "start": 776.0252499999999,
                "end": 783.0739583333333,
                "name": 'eyecatcher'
                },
                {
                "start": 783.0739583333333,
                "end": 790.5397499999999,
                "name": 'eyecatcher'
                },
                {
                "start": 790.5397499999999,
                "end": 1390.0553333333332,
                "name": 'segment'
                },
                {
                "start": 1390.0553333333332,
                "end": 1390.0553333333332,
                "name": 'easeout'
                },
                {
                "start": 1390.0553333333332,
                "end": 1460.0419166666666,
                "name": 'themeclose'
                },
                {
                "start": 1460.0419166666666,
                "end": 1490.0719166666665,
                "name": 'teaser'
                },
                {
                "start": 1490.0719166666665,
                "end": 1500.217,
                "name": 'signoff'
                },
            ]
        },
        {
            "name": "Drum Island",
            "startend": [78,91],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 644.018375,
                "name": 'segment'
                },
                {
                "start": 644.018375,
                "end": 651.1087916666667,
                "name": 'eyecatcher'
                },
                {
                "start": 651.1087916666667,
                "end": 658.5745833333333,
                "name": 'eyecatcher'
                },
                {
                "start": 658.5745833333333,
                "end": 1329.07775,
                "name": 'segment'
                },
                {
                "start": 1329.07775,
                "end": 1329.07775,
                "name": 'easeout'
                },
                {
                "start": 1329.07775,
                "end": 1400.1070416666666,
                "name": 'themeclose'
                },
                {
                "start": 1400.1070416666666,
                "end": 1430.0953333333332,
                "name": 'teaser'
                },
                {
                "start": 1430.0953333333332,
                "end": 1440.189,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Alabasta",
            "startend": [92,130],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 713.0039583333332,
                "name": 'segment'
                },
                {
                "start": 713.0039583333332,
                "end": 720.0526666666666,
                "name": 'eyecatcher'
                },
                {
                "start": 720.0526666666666,
                "end": 727.5184583333332,
                "name": 'eyecatcher'
                },
                {
                "start": 727.5184583333332,
                "end": 1328.9943333333333,
                "name": 'segment'
                },
                {
                "start": 1328.9943333333333,
                "end": 1328.9943333333333,
                "name": 'easeout'
                },
                {
                "start": 1328.9943333333333,
                "end": 1400.0236249999998,
                "name": 'themeclose'
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser'
                },
                {
                "start": 1430.053625,
                "end": 1440.192,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Post-Alabasta, Pre-Jaya",
            "startend": [131,143],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.91645833333332,
                "name": 'themeopen'
                },
                {
                "start": 124.91645833333332,
                "end": 124.91645833333332,
                "name": 'easein'
                },
                {
                "start": 124.91645833333332,
                "end": 694.7774166666666,
                "name": 'segment'
                },
                {
                "start": 694.7774166666666,
                "end": 701.7844166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 701.7844166666666,
                "end": 709.2502083333333,
                "name": 'eyecatcher'
                },
                {
                "start": 709.2502083333333,
                "end": 1328.7857916666667,
                "name": 'segment'
                },
                {
                "start": 1328.7857916666667,
                "end": 1328.7857916666667,
                "name": 'easeout'
                },
                {
                "start": 1328.7857916666667,
                "end": 1400.7326666666665,
                "name": 'themeclose'
                },
                {
                "start": 1400.7326666666665,
                "end": 1430.6375416666665,
                "name": 'teaser'
                },
                {
                "start": 1430.6375416666665,
                "end": 1440.147,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Skypiea",
            "startend": [144,195],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.91645833333332,
                "name": 'themeopen'
                },
                {
                "start": 124.91645833333332,
                "end": 124.91645833333332,
                "name": 'easein'
                },
                {
                "start": 124.91645833333332,
                "end": 835.8767083333332,
                "name": 'segment'
                },
                {
                "start": 835.8767083333332,
                "end": 842.8837083333333,
                "name": 'eyecatcher'
                },
                {
                "start": 842.8837083333333,
                "end": 850.3077916666666,
                "name": 'eyecatcher'
                },
                {
                "start": 850.3077916666666,
                "end": 1328.8274999999999,
                "name": 'segment'
                },
                {
                "start": 1328.8274999999999,
                "end": 1328.8274999999999,
                "name": 'easeout'
                },
                {
                "start": 1328.8274999999999,
                "end": 1400.64925,
                "name": 'themeclose'
                },
                {
                "start": 1400.64925,
                "end": 1430.5541249999999,
                "name": 'teaser'
                },
                {
                "start": 1430.5541249999999,
                "end": 1440.239,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "G8, Long Ring",
            "startend": [196,228],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 626.000375,
                "name": 'segment'
                },
                {
                "start": 626.000375,
                "end": 633.0907916666666,
                "name": 'eyecatcher'
                },
                {
                "start": 633.0907916666666,
                "end": 640.5565833333333,
                "name": 'eyecatcher'
                },
                {
                "start": 640.5565833333333,
                "end": 1329.07775,
                "name": 'segment'
                },
                {
                "start": 1329.07775,
                "end": 1329.07775,
                "name": 'easeout'
                },
                {
                "start": 1329.07775,
                "end": 1400.0653333333332,
                "name": 'themeclose'
                },
                {
                "start": 1400.0653333333332,
                "end": 1430.0119166666666,
                "name": 'teaser'
                },
                {
                "start": 1430.0119166666666,
                "end": 1440.239,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Water Seven",
            "startend": [229,263],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 630.9636666666667,
                "name": 'segment'
                },
                {
                "start": 630.9636666666667,
                "end": 638.0123749999999,
                "name": 'eyecatcher'
                },
                {
                "start": 638.0123749999999,
                "end": 645.519875,
                "name": 'eyecatcher'
                },
                {
                "start": 645.519875,
                "end": 1329.0360416666665,
                "name": 'segment'
                },
                {
                "start": 1329.0360416666665,
                "end": 1329.0360416666665,
                "name": 'easeout'
                },
                {
                "start": 1329.0360416666665,
                "end": 1400.0236249999998,
                "name": 'themeclose'
                },
                {
                "start": 1400.0236249999998,
                "end": 1429.9702083333332,
                "name": 'teaser'
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.123,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Enies Lobby",
            "startend": [264,278],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 203.99545833333332,
                "name": 'easein'
                },
                {
                "start": 203.99545833333332,
                "end": 314.02204166666667,
                "name": 'themeopen'
                },
                {
                "start": 314.02204166666667,
                "end": 745.9952499999999,
                "name": 'segment'
                },
                {
                "start": 745.9952499999999,
                "end": 753.0856666666666,
                "name": 'eyecatcher'
                },
                {
                "start": 753.0856666666666,
                "end": 760.5931666666667,
                "name": 'eyecatcher'
                },
                {
                "start": 760.5931666666667,
                "end": 1319.1094583333334,
                "name": 'segment'
                },
                {
                "start": 1319.1094583333334,
                "end": 1319.1094583333334,
                "name": 'easeout'
                },
                {
                "start": 1319.1094583333334,
                "end": 1390.0970416666667,
                "name": 'themeclose'
                },
                {
                "start": 1390.0970416666667,
                "end": 1420.0436249999998,
                "name": 'teaser'
                },
                {
                "start": 1420.0436249999998,
                "end": 1430.232,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Enies Lobby - Straw Hat Theater",
            "startend": [279,283],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 409.36729166666663,
                "name": 'easein'
                },
                {
                "start": 409.36729166666663,
                "end": 828.0355416666666,
                "name": 'segment'
                },
                {
                "start": 828.0355416666666,
                "end": 835.0425416666666,
                "name": 'eyecatcher'
                },
                {
                "start": 835.0425416666666,
                "end": 842.5500416666666,
                "name": 'eyecatcher'
                },
                {
                "start": 842.5500416666666,
                "end": 1229.97875,
                "name": 'segment'
                },
                {
                "start": 1229.97875,
                "end": 1229.97875,
                "name": 'easeout'
                },
                {
                "start": 1229.97875,
                "end": 1400.1070416666666,
                "name": 'extra'
                },
                {
                "start": 1400.1070416666666,
                "end": 1430.1370416666666,
                "name": 'teaser'
                },
                {
                "start": 1430.1370416666666,
                "end": 1440.262,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Enies Lobby - last half",
            "startend": [284,336],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen'
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'easein'
                },
                {
                "start": 124.99987499999999,
                "end": 907.9487083333332,
                "name": 'segment'
                },
                {
                "start": 907.9487083333332,
                "end": 914.9974166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 914.9974166666666,
                "end": 922.4632083333332,
                "name": 'eyecatcher'
                },
                {
                "start": 922.4632083333332,
                "end": 1360.0253333333333,
                "name": 'segment'
                },
                {
                "start": 1360.0253333333333,
                "end": 1360.0253333333333,
                "name": 'easeout'
                },
                {
                "start": 1360.0253333333333,
                "end": 1390.0553333333332,
                "name": 'teaser'
                },
                {
                "start": 1390.0553333333332,
                "end": 1400.231,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Thriller Bark",
            "startend": [337,381],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'easein'
                },
                {
                "start": 164.99816666666666,
                "end": 828.0355416666666,
                "name": 'segment'
                },
                {
                "start": 828.0355416666666,
                "end": 835.0425416666666,
                "name": 'eyecatcher'
                },
                {
                "start": 835.0425416666666,
                "end": 842.5083333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 842.5083333333333,
                "end": 1400.0236249999998,
                "name": 'segment'
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout'
                },
                {
                "start": 1400.0236249999998,
                "end": 1429.9702083333332,
                "name": 'teaser'
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.123,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Sabaody Archipelago",
            "startend": [382,407],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'easein'
                },
                {
                "start": 164.99816666666666,
                "end": 902.9854166666667,
                "name": 'segment'
                },
                {
                "start": 902.9854166666667,
                "end": 909.9924166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 909.9924166666666,
                "end": 917.4999166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 917.4999166666666,
                "end": 1399.9819166666666,
                "name": 'segment'
                },
                {
                "start": 1399.9819166666666,
                "end": 1399.9819166666666,
                "name": 'easeout'
                },
                {
                "start": 1399.9819166666666,
                "end": 1429.9702083333332,
                "name": 'teaser'
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.03,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Island of Women",
            "startend": [408,422],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'easein'
                },
                {
                "start": 164.99816666666666,
                "end": 927.051125,
                "name": 'segment'
                },
                {
                "start": 927.051125,
                "end": 933.9747083333333,
                "name": 'eyecatcher'
                },
                {
                "start": 933.9747083333333,
                "end": 941.4822083333332,
                "name": 'eyecatcher'
                },
                {
                "start": 941.4822083333332,
                "end": 1394.9769166666665,
                "name": 'segment'
                },
                {
                "start": 1394.9769166666665,
                "end": 1394.9769166666665,
                "name": 'easeout'
                },
                {
                "start": 1394.9769166666665,
                "end": 1425.0069166666665,
                "name": 'teaser'
                },
                {
                "start": 1425.0069166666665,
                "end": 1435.108,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Impel Down",
            "startend": [423,456],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'easein'
                },
                {
                "start": 164.99816666666666,
                "end": 885.9684166666666,
                "name": 'segment'
                },
                {
                "start": 885.9684166666666,
                "end": 892.9754166666665,
                "name": 'eyecatcher'
                },
                {
                "start": 892.9754166666665,
                "end": 900.4829166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 900.4829166666666,
                "end": 1394.9769166666665,
                "name": 'segment'
                },
                {
                "start": 1394.9769166666665,
                "end": 1394.9769166666665,
                "name": 'easeout'
                },
                {
                "start": 1394.9769166666665,
                "end": 1424.9652083333333,
                "name": 'teaser'
                },
                {
                "start": 1424.9652083333333,
                "end": 1435.107,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Marineford",
            "startend": [457,516],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'easein'
                },
                {
                "start": 164.99816666666666,
                "end": 877.0428333333333,
                "name": 'segment'
                },
                {
                "start": 877.0428333333333,
                "end": 883.9664166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 883.9664166666666,
                "end": 891.4739166666666,
                "name": 'eyecatcher'
                },
                {
                "start": 891.4739166666666,
                "end": 1400.0236249999998,
                "name": 'segment'
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout'
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser'
                },
                {
                "start": 1430.053625,
                "end": 1440.146,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Fishman Island",
            "startend": [517,578],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.95645833333333,
                "name": 'themeopen'
                },
                {
                "start": 164.95645833333333,
                "end": 301.00904166666663,
                "name": 'easein'
                },
                {
                "start": 301.00904166666663,
                "end": 861.9861249999999,
                "name": 'segment'
                },
                {
                "start": 861.9861249999999,
                "end": 869.0348333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 869.0348333333333,
                "end": 876.5423333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 876.5423333333333,
                "end": 1400.0236249999998,
                "name": 'segment'
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout'
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser'
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.192,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Punk Hazard",
            "startend": [579,628],
            "cut_segments": [
                {
                "start": 0,
                "end": 150.01653333333334,
                "name": 'themeopen'
                },
                {
                "start": 150.01653333333334,
                "end": 313.98033333333336,
                "name": 'easein'
                },
                {
                "start": 313.98033333333336,
                "end": 819.9858333333334,
                "name": 'segment'
                },
                {
                "start": 819.9858333333334,
                "end": 826.9261,
                "name": 'eyecatcher'
                },
                {
                "start": 826.9261,
                "end": 834.4336000000001,
                "name": 'eyecatcher'
                },
                {
                "start": 834.4336000000001,
                "end": 1384.9502333333335,
                "name": 'segment'
                },
                {
                "start": 1384.9502333333335,
                "end": 1384.9502333333335,
                "name": 'easeout'
                },
                {
                "start": 1384.9502333333335,
                "end": 1414.9802333333334,
                "name": 'teaser'
                },
                {
                "start": 1414.9802333333334,
                "end": 1432.248,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Dressrosa",
            "startend": [629,746],
            "cut_segments": [
                {
                "start": 0,
                "end": 150.01653333333334,
                "name": 'themeopen'
                },
                {
                "start": 150.01653333333334,
                "end": 239.5393,
                "name": 'easein'
                },
                {
                "start": 239.5393,
                "end": 826.9928333333334,
                "name": 'segment'
                },
                {
                "start": 826.9928333333334,
                "end": 833.9998333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 833.9998333333333,
                "end": 841.5073333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 841.5073333333333,
                "end": 1384.9502333333335,
                "name": 'segment'
                },
                {
                "start": 1384.9502333333335,
                "end": 1384.9502333333335,
                "name": 'easeout'
                },
                {
                "start": 1384.9502333333335,
                "end": 1414.9802333333334,
                "name": 'teaser'
                },
                {
                "start": 1414.9802333333334,
                "end": 1431.268,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Zou",
            "startend": [747,782],
            "cut_segments": [
                {
                "start": 0,
                "end": 14.973291666666666,
                "name": 'production'
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen'
                },
                {
                "start": 164.99816666666666,
                "end": 419.66925,
                "name": 'easein'
                },
                {
                "start": 419.66925,
                "end": 864.0298333333333,
                "name": 'segment'
                },
                {
                "start": 864.0298333333333,
                "end": 871.0368333333332,
                "name": 'eyecatcher'
                },
                {
                "start": 871.0368333333332,
                "end": 878.5443333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 878.5443333333333,
                "end": 1400.0236249999998,
                "name": 'segment'
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout'
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser'
                },
                {
                "start": 1430.053625,
                "end": 1446.417,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Whole Cake Island",
            "startend": [783,891],
            "cut_segments": [
                {
                "start": 0,
                "end": 149.98316666666665,
                "name": 'themeopen'
                },
                {
                "start": 149.98316666666665,
                "end": 276.6869791666667,
                "name": 'easein'
                },
                {
                "start": 276.6869791666667,
                "end": 814.9808333333333,
                "name": 'segment'
                },
                {
                "start": 814.9808333333333,
                "end": 821.9878333333332,
                "name": 'eyecatcher'
                },
                {
                "start": 821.9878333333332,
                "end": 829.4953333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 829.4953333333333,
                "end": 1384.9669166666665,
                "name": 'segment'
                },
                {
                "start": 1384.9669166666665,
                "end": 1384.9669166666665,
                "name": 'easeout'
                },
                {
                "start": 1384.9669166666665,
                "end": 1414.9969166666665,
                "name": 'teaser'
                },
                {
                "start": 1414.9969166666665,
                "end": 1417.25,
                "name": 'signoff'
                }
            ]
        },
        {
            "name": "Wano Country",
            "startend": [892,991],
            "cut_segments": [
                {
                "start": 0,
                "end": 10.468791666666666,
                "name": 'production'
                },
                {
                "start": 10.468791666666666,
                "end": 130.58879166666665,
                "name": 'themeopen'
                },
                {
                "start": 130.58879166666665,
                "end": 196.61308333333332,
                "name": 'easein'
                },
                {
                "start": 196.61308333333332,
                "end": 906.5723333333333,
                "name": 'segment'
                },
                {
                "start": 906.5723333333333,
                "end": 913.5793333333332,
                "name": 'eyecatcher'
                },
                {
                "start": 913.5793333333332,
                "end": 921.0868333333333,
                "name": 'eyecatcher'
                },
                {
                "start": 921.0868333333333,
                "end": 1395.5191249999998,
                "name": 'segment'
                },
                {
                "start": 1395.5191249999998,
                "end": 1395.5191249999998,
                "name": 'easeout'
                },
                {
                "start": 1395.5191249999998,
                "end": 1425.549125,
                "name": 'teaser'
                },
                {
                "start": 1425.549125,
                "end": 1442.045,
                "name": 'signoff'
                }
            ]
        }
    ]    
}

def find_files_for_projgen(root: Path):
    """
    walks the target directory for pairs of matching video and LosslessCut project files.
    (0001.mkv, 0001-proj.llc) qualifies as a pair
    in order to generate a file, the walk must find
    a: an mkv file that meets naming scheme (TODO set a naming scheme)
    b: there is NOT already a LLC file for this file
    c: there is NOT already a rendered video in the same directory
    """
    pairs = []
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        for filename in filenames:
            # skip file if it is not an uncut mkv video
            if not filename.lower().endswith(".mkv") or filename.lower().endswith("-cut.mkv"):
                continue
            # get a list of files in the current dir to check against
            files_in_dir = os.listdir(dirpath)
            filename_base = filename[:-4]
            skip = False
            for f in files_in_dir:
                if f == f"{filename_base}-proj.llc" or f ==f"{filename_base}-PROJGEN.llc" or f ==f"{filename_base}-cut.mkv":
                    skip = True
                    break
            if skip is False:
                pairs.append(dirpath / filename)
    return sorted(pairs)

def get_target_dir():
    """Setting the cwd. Can be set automatically or by the user."""
    target_dir = ""
    if len(sys.argv) == 1: #no args
        target_dir = os.getcwd()
    elif len(sys.argv) == 2: #one arg
        target_dir = os.path.abspath(sys.argv[1])
    else:
        print("Usage: py main.py [DIRECTORY]")
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory")
        sys.exit(1)
    else:
        return target_dir

def get_video_length(filename):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True)
    return float(result.stdout)

def get_episode_number(file):
    filename_base = os.path.splitext(os.path.basename(file))[0]
    m = re.search(r"\d{4}", filename_base).group()
    return int(m.lstrip("0"))

def get_template_by_episode(ep):
    templates = TEMPLATES["OnePiece"]

    results = []
    for i, x in enumerate(templates):
        start = x["startend"][0]
        end = x["startend"][1]
        if start <= ep and end >= ep:
            results.append(i)
    if len(results) == 1:
        return results[0]
    else:
        print(f"WARN: Episode number [{ep}] does not match any template. Using the first template.")
        return 0

def generate_proj(filepath, vid_len, episode_num):
    """generates a LosslessCut project file, scaling the template to
    fit the video. This does NOT create a perfect cut, it only places
    all segments in the correct order at an approximate size"""
    proj_json = {}
    proj_json["version"] = 2
    proj_json["mediaFileName"] = os.path.basename(filepath)
    cut_segments = []
    template_index = get_template_by_episode(episode_num)
    template_len = TEMPLATES["OnePiece"][template_index]["cut_segments"][-1]["end"]
    scale = vid_len / template_len
    segments_total_len = 0.0

    for s in TEMPLATES["OnePiece"][template_index]["cut_segments"]:
        temp_start = s["start"]
        temp_end = s["end"]
        segment_len = temp_end - temp_start

        segment_scaled_len = segment_len * scale
        cut_segments.append({
            "start": segments_total_len,
            "end": segments_total_len + segment_scaled_len,
            "name": s["name"],
            "selected": True
        })
        print(f"{segments_total_len} + {segment_scaled_len} = {segments_total_len + segment_scaled_len}")
        segments_total_len += segment_scaled_len
    proj_json["cutSegments"] = cut_segments

    if not math.isclose(segments_total_len, vid_len):
        print(f"WARN: {os.path.basename(filepath)} does not scale properly ({segments_total_len} != {vid_len}).")
        print(f"{os.path.basename(filepath)} project not generated.")
        return
    
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(os.path.splitext(filepath)[0])
    new_filename = f"{file_name}-PROJGEN.llc"
    with open(os.path.join(file_dir, new_filename), "w", encoding="utf-8") as proj:
        json.dump(proj_json, proj, ensure_ascii=False, indent=4)

def main():
    """main."""
    # check for dependencies
    has_ffprobe = Utils.check_dependency("ffprobe")
    if not has_ffprobe:
        sys.exit(1)

    target_dir = get_target_dir()

    print(f"Recursively searching: {target_dir}")
    noprojfiles = find_files_for_projgen(target_dir)
    if not noprojfiles:
        print("No file found for projgen.")
        return
    else:
        print(f"Found {len(noprojfiles)} files for projgen.")
    for f in noprojfiles:
        vid_len = get_video_length(f)
        ep = get_episode_number(f)
        generate_proj(f, vid_len, ep)


    print("\nDone.")

if __name__ == "__main__":
    main()