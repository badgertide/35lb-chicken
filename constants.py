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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 134.59239527777777,
                "end": 134.59239527777777,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 171.25441666666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 176.2618675,
                "end": 176.2618675,
                "name": 'titlecard',
                "stretch": False
                },
                {
                "start": 180.26341666666664,
                "end": 722.0129583333332,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 722.0129583333332,
                "end": 729.0616666666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 729.0616666666666,
                "end": 736.5274583333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 736.5274583333332,
                "end": 1387.010625,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1387.010625,
                "end": 1387.010625,
                "name": 'easeout',
                "stretch": False
                },
                {
                "start": 1387.010625,
                "end": 1390.0136249999998,
                "name": 'tbc',
                "stretch": False,
                },
                {
                "start": 1390.0136249999998,
                "end": 1460.0002083333331,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1460.0002083333331,
                "end": 1489.9885,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1489.9885,
                "end": 1500.0302083333331,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.95816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.95816666666666,
                "end": 124.95816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.95816666666666,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 776.0252499999999,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 776.0252499999999,
                "end": 783.0739583333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 783.0739583333333,
                "end": 790.5397499999999,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 790.5397499999999,
                "end": 1390.0553333333332,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1390.0553333333332,
                "end": 1390.0553333333332,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1390.0553333333332,
                "end": 1460.0419166666666,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1460.0419166666666,
                "end": 1490.0719166666665,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1490.0719166666665,
                "end": 1500.217,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 644.018375,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 644.018375,
                "end": 651.1087916666667,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 651.1087916666667,
                "end": 658.5745833333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 658.5745833333333,
                "end": 1329.07775,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1329.07775,
                "end": 1329.07775,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1329.07775,
                "end": 1400.1070416666666,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.1070416666666,
                "end": 1430.0953333333332,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.0953333333332,
                "end": 1440.189,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 713.0039583333332,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 713.0039583333332,
                "end": 720.0526666666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 720.0526666666666,
                "end": 727.5184583333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 727.5184583333332,
                "end": 1328.9943333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1328.9943333333333,
                "end": 1328.9943333333333,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1328.9943333333333,
                "end": 1400.0236249999998,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.053625,
                "end": 1440.192,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.91645833333332,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.91645833333332,
                "end": 124.91645833333332,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.91645833333332,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 694.7774166666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 694.7774166666666,
                "end": 701.7844166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 701.7844166666666,
                "end": 709.2502083333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 709.2502083333333,
                "end": 1328.7857916666667,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1328.7857916666667,
                "end": 1328.7857916666667,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1328.7857916666667,
                "end": 1400.7326666666665,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.7326666666665,
                "end": 1430.6375416666665,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.6375416666665,
                "end": 1440.147,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.91645833333332,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.91645833333332,
                "end": 124.91645833333332,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.91645833333332,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 835.8767083333332,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 835.8767083333332,
                "end": 842.8837083333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 842.8837083333333,
                "end": 850.3077916666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 850.3077916666666,
                "end": 1328.8274999999999,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1328.8274999999999,
                "end": 1328.8274999999999,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1328.8274999999999,
                "end": 1400.64925,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.64925,
                "end": 1430.5541249999999,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.5541249999999,
                "end": 1440.239,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 626.000375,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 626.000375,
                "end": 633.0907916666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 633.0907916666666,
                "end": 640.5565833333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 640.5565833333333,
                "end": 1329.07775,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1329.07775,
                "end": 1329.07775,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1329.07775,
                "end": 1400.0653333333332,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.0653333333332,
                "end": 1430.0119166666666,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.0119166666666,
                "end": 1440.239,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 630.9636666666667,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 630.9636666666667,
                "end": 638.0123749999999,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 638.0123749999999,
                "end": 645.519875,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 645.519875,
                "end": 1329.0360416666665,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1329.0360416666665,
                "end": 1329.0360416666665,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1329.0360416666665,
                "end": 1400.0236249999998,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1400.0236249999998,
                "end": 1429.9702083333332,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.123,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 203.99545833333332,
                "name": 'recap',
                "stretch": False
                },
                {
                "start": 203.99545833333332,
                "end": 314.02204166666667,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 314.02204166666667,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 745.9952499999999,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 745.9952499999999,
                "end": 753.0856666666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 753.0856666666666,
                "end": 760.5931666666667,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 760.5931666666667,
                "end": 1319.1094583333334,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1319.1094583333334,
                "end": 1319.1094583333334,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1319.1094583333334,
                "end": 1390.0970416666667,
                "name": 'themeclose',
                "stretch": False
                },
                {
                "start": 1390.0970416666667,
                "end": 1420.0436249999998,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1420.0436249999998,
                "end": 1430.232,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 409.36729166666663,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 409.36729166666663,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 828.0355416666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 828.0355416666666,
                "end": 835.0425416666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 835.0425416666666,
                "end": 842.5500416666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 842.5500416666666,
                "end": 1229.97875,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1229.97875,
                "end": 1229.97875,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1229.97875,
                "end": 1400.1070416666666,
                "name": 'extra',
                "stretch": True
                },
                {
                "start": 1400.1070416666666,
                "end": 1430.1370416666666,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.1370416666666,
                "end": 1440.262,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 124.99987499999999,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 124.99987499999999,
                "end": 124.99987499999999,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 124.99987499999999,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 907.9487083333332,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 907.9487083333332,
                "end": 914.9974166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 914.9974166666666,
                "end": 922.4632083333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 922.4632083333332,
                "end": 1360.0253333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1360.0253333333333,
                "end": 1360.0253333333333,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1360.0253333333333,
                "end": 1390.0553333333332,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1390.0553333333332,
                "end": 1400.231,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 164.99816666666666,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 828.0355416666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 828.0355416666666,
                "end": 835.0425416666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 835.0425416666666,
                "end": 842.5083333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 842.5083333333333,
                "end": 1400.0236249999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1429.9702083333332,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.123,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 164.99816666666666,
                "end": 158.65849999999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 158.65849999999998,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 902.9854166666667,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 902.9854166666667,
                "end": 909.9924166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 909.9924166666666,
                "end": 917.4999166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 917.4999166666666,
                "end": 1399.9819166666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1399.9819166666666,
                "end": 1399.9819166666666,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1399.9819166666666,
                "end": 1429.9702083333332,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1429.9702083333332,
                "end": 1440.03,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 164.99816666666666,
                "end": 165.99816666666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 165.99816666666666,
                "end": 167.70920833333332,
                "name": 'titlecard',
                "stretch": True
                },
                {
                "start": 167.70920833333332,
                "end": 927.051125,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 927.051125,
                "end": 933.9747083333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 933.9747083333333,
                "end": 941.4822083333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 941.4822083333332,
                "end": 1394.9769166666665,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1394.9769166666665,
                "end": 1394.9769166666665,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1394.9769166666665,
                "end": 1425.0069166666665,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1425.0069166666665,
                "end": 1435.108,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 164.99816666666666,
                "end": 885.9684166666666,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 885.9684166666666,
                "end": 892.9754166666665,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 892.9754166666665,
                "end": 900.4829166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 900.4829166666666,
                "end": 1394.9769166666665,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1394.9769166666665,
                "end": 1394.9769166666665,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1394.9769166666665,
                "end": 1424.9652083333333,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1424.9652083333333,
                "end": 1435.107,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 164.99816666666666,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 164.99816666666666,
                "end": 877.0428333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 877.0428333333333,
                "end": 883.9664166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 883.9664166666666,
                "end": 891.4739166666666,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 891.4739166666666,
                "end": 1400.0236249999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.053625,
                "end": 1440.146,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.95645833333333,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.95645833333333,
                "end": 301.00904166666663,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 301.00904166666663,
                "end": 861.9861249999999,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 861.9861249999999,
                "end": 869.0348333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 869.0348333333333,
                "end": 876.5423333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 876.5423333333333,
                "end": 1400.0236249999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.053625,
                "end": 1440.192,
                "name": 'signoff',
                "stretch": False
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
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 150.01653333333334,
                "end": 313.98033333333336,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 313.98033333333336,
                "end": 819.9858333333334,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 819.9858333333334,
                "end": 826.9261,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 826.9261,
                "end": 834.4336000000001,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 834.4336000000001,
                "end": 1384.9502333333335,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1384.9502333333335,
                "end": 1384.9502333333335,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1384.9502333333335,
                "end": 1414.9802333333334,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1414.9802333333334,
                "end": 1432.248,
                "name": 'signoff',
                "stretch": False
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
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 150.01653333333334,
                "end": 239.5393,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 239.5393,
                "end": 826.9928333333334,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 826.9928333333334,
                "end": 833.9998333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 833.9998333333333,
                "end": 841.5073333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 841.5073333333333,
                "end": 1384.9502333333335,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1384.9502333333335,
                "end": 1384.9502333333335,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1384.9502333333335,
                "end": 1414.9802333333334,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1414.9802333333334,
                "end": 1431.268,
                "name": 'signoff',
                "stretch": False
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
                "name": 'production',
                "stretch": False
                },
                {
                "start": 14.973291666666666,
                "end": 164.99816666666666,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 164.99816666666666,
                "end": 419.66925,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 419.66925,
                "end": 864.0298333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 864.0298333333333,
                "end": 871.0368333333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 871.0368333333332,
                "end": 878.5443333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 878.5443333333333,
                "end": 1400.0236249999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1400.0236249999998,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1400.0236249999998,
                "end": 1430.053625,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1430.053625,
                "end": 1446.417,
                "name": 'signoff',
                "stretch": False
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
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 149.98316666666665,
                "end": 276.6869791666667,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 276.6869791666667,
                "end": 814.9808333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 814.9808333333333,
                "end": 821.9878333333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 821.9878333333332,
                "end": 829.4953333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 829.4953333333333,
                "end": 1384.9669166666665,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1384.9669166666665,
                "end": 1384.9669166666665,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1384.9669166666665,
                "end": 1414.9969166666665,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1414.9969166666665,
                "end": 1417.25,
                "name": 'signoff',
                "stretch": False
                }
            ]
        },
        {
            "name": "Wano Country",
            "startend": [892,1071],
            "cut_segments": [
                {
                "start": 0,
                "end": 10.468791666666666,
                "name": 'production',
                "stretch": False
                },
                {
                "start": 10.468791666666666,
                "end": 130.58879166666665,
                "name": 'themeopen',
                "stretch": False
                },
                {
                "start": 130.58879166666665,
                "end": 196.61308333333332,
                "name": 'recap',
                "stretch": True
                },
                {
                "start": 196.61308333333332,
                "end": 906.5723333333333,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 906.5723333333333,
                "end": 913.5793333333332,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 913.5793333333332,
                "end": 921.0868333333333,
                "name": 'eyecatcher',
                "stretch": False
                },
                {
                "start": 921.0868333333333,
                "end": 1395.5191249999998,
                "name": 'generic',
                "stretch": True
                },
                {
                "start": 1395.5191249999998,
                "end": 1395.5191249999998,
                "name": 'easeout',
                "stretch": True
                },
                {
                "start": 1395.5191249999998,
                "end": 1425.549125,
                "name": 'teaser',
                "stretch": False
                },
                {
                "start": 1425.549125,
                "end": 1442.045,
                "name": 'signoff',
                "stretch": False
                }
            ]
        }
    ]    
}

CUT_FILE_PREFIX = "35pc-"
LOSSLESSCUT_SUFFIX = "-proj.llc"

FILLER_TYPES = ["filler"]
MAX_LOOPS = 10000

