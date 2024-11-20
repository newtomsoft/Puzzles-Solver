import webbrowser

from GridProviders.StringGridProvider import StringGridProvider
from PuzzleNorinoriGridProvider import PuzzleNorinoriGridProvider
from Puzzles.Norinori.NorinoriGame import NorinoriGame
from Utils.Grid import Grid


class NorinoriMainConsole:
    @staticmethod
    def main():
        grid = NorinoriMainConsole.get_grid()
        NorinoriMainConsole.run(grid)

    @staticmethod
    def get_grid():
        print("Norinori Game")
        print("Enter url or grid")
        console_input = input()
        url_patterns = {
            r"https://fr.puzzle-norinori.com/": PuzzleNorinoriGridProvider,
            r"https://www.puzzle-norinori.com/": PuzzleNorinoriGridProvider
        }

        for pattern, provider_class in url_patterns.items():
            if pattern in console_input:
                provider = provider_class()
                return provider.get_grid(console_input)

        return StringGridProvider().get_grid(console_input)

    @staticmethod
    def run(grid: Grid):
        try:
            game = NorinoriGame(grid)
        except ValueError as e:
            print(f"Error: {e}")
            return
        solution_grid = game.get_solution()
        if solution_grid:
            print(f"Solution found")
            printable_grid = Grid([['■' if solution_grid.value(r, c) else ' ' for c in range(grid.columns_number)] for r in range(grid.rows_number)])
            police_color_grid = Grid([[16 for _ in range(grid.columns_number)] for _ in range(grid.rows_number)])
            printable_grid_string = printable_grid.to_console_string(police_color_grid, grid)
            print(printable_grid_string)
            NorinoriMainConsole.generate_html(grid, solution_grid)
        else:
            print(f"No solution found")

    @staticmethod
    def generate_html(grid: Grid, solution_grid: Grid):
        color_map = {
            0: "#bba3e2",
            1: "#ffc992",
            2: "#96beff",
            3: "#b3dfa0",
            4: "#dfdfdf",
            5: "#ff7b60",
            6: "#e6f388",
            7: "#b9b29e",
            8: "#dfa0bf",
            9: "#a3d2d8",
            10: "#62efea",
            'A': "#62efea",
            11: "#ff93f3",
            'B': "#ff93f3",
            12: "#8acc6d",
            'C': "#8acc6d",
            13: "#729aec",
            'D': "#729aec",
            14: "#c387e0",
            'E': "#c387e0",
            15: "#ffe04b",
            'F': "#ffe04b",
            16: "#ff6347",
            'G': "#ff6347",
            17: "#4682b4",
            'H': "#4682b4",
            18: "#32cd32",
            'I': "#32cd32",
            19: "#ff4500",
            'J': "#ff4500",
            20: "#6a5acd",
            'K': "#6a5acd",
            21: "#ff1493",
            'L': "#ff1493",
            22: "#00ced1",
            23: "#00ffff",  # Aqua
            24: "#f0f8ff",  # Alice Blue
            25: "#faebd7",  # Antique White
            26: "#ff7f50",  # Coral
            27: "#6495ed",  # Cornflower Blue
            28: "#fff8dc",  # Cornsilk
            29: "#dc143c",  # Crimson
            30: "#00ffff",  # Cyan
            31: "#00008b",  # Dark Blue
            32: "#008b8b",  # Dark Cyan
            33: "#b8860b",  # Dark Goldenrod
            34: "#a9a9a9",  # Dark Gray
            35: "#006400",  # Dark Green
            36: "#bdb76b",  # Dark Khaki
            37: "#8b008b",  # Dark Magenta
            38: "#556b2f",  # Dark Olive Green
            39: "#ff8c00",  # Dark Orange
            40: "#9932cc",  # Dark Orchid
            41: "#8b0000",  # Dark Red
            42: "#e9967a",  # Dark Salmon
            43: "#8fbc8f",  # Dark Sea Green
            44: "#483d8b",  # Dark Slate Blue
            45: "#2f4f4f",  # Dark Slate Gray
            46: "#00ced1",  # Dark Turquoise
            47: "#9400d3",  # Dark Violet
            48: "#ff1493",  # Deep Pink
            49: "#00bfff",  # Deep Sky Blue
            50: "#696969",  # Dim Gray
            51: "#1e90ff",  # Dodger Blue
            52: "#b22222",  # Firebrick
            53: "#fffaf0",  # Floral White
            54: "#228b22",  # Forest Green
            55: "#dcdcdc",  # Gainsboro
            56: "#f8f8ff",  # Ghost White
            57: "#ffd700",  # Gold
            58: "#daa520",  # Goldenrod
            59: "#808080",  # Gray
            60: "#008000",  # Green
            61: "#adff2f",  # Green Yellow
            62: "#f0fff0",  # Honeydew
            63: "#ff69b4",  # Hot Pink
            64: "#cd5c5c",  # Indian Red
            65: "#4b0082",  # Indigo
            66: "#fffff0",  # Ivory
            67: "#f0e68c",  # Khaki
            68: "#e6e6fa",  # Lavender
            69: "#fff0f5",  # Lavender Blush
            70: "#7cfc00",  # Lawn Green
            71: "#fffacd",  # Lemon Chiffon
            72: "#add8e6",  # Light Blue
            73: "#f08080",  # Light Coral
            74: "#e0ffff",  # Light Cyan
            75: "#fafad2",  # Light Goldenrod Yellow
            76: "#d3d3d3",  # Light Gray
            77: "#ffb6c1",  # Light Pink
            78: "#ffa07a",  # Light Salmon
            79: "#20b2aa",  # Light Sea Green
            80: "#87cefa",  # Light Sky Blue
            81: "#778899",  # Light Slate Gray
            82: "#b0c4de",  # Light Steel Blue
            83: "#ffffe0",  # Light Yellow
            84: "#32cd32",  # Lime Green
            85: "#faf0e6",  # Linen
            86: "#ff00ff",  # Magenta
            87: "#800000",  # Maroon
            88: "#66cdaa",  # Medium Aquamarine
            89: "#0000cd",  # Medium Blue
            90: "#ba55d3",  # Medium Orchid
            91: "#9370db",  # Medium Purple
            92: "#3cb371",  # Medium Sea Green
            93: "#7b68ee",  # Medium Slate Blue
            94: "#00fa9a",  # Medium Spring Green
            95: "#48d1cc",  # Medium Turquoise
            96: "#c71585",  # Medium Violet Red
            97: "#191970",  # Midnight Blue
            98: "#f5fffa",  # Mint Cream
            99: "#ffe4e1",  # Misty Rose
            100: "#ffe4b5",  # Moccasin
            101: "#ffdead",  # Navajo White
            102: "#000080",  # Navy
            103: "#fdf5e6",  # Old Lace
            104: "#808000",  # Olive
            105: "#6b8e23",  # Olive Drab
            106: "#ffa500",  # Orange
            107: "#ff4500",  # Orange Red
            108: "#da70d6",  # Orchid
            109: "#eee8aa",  # Pale Goldenrod
            110: "#98fb98",  # Pale Green
            111: "#afeeee",  # Pale Turquoise
            112: "#db7093",  # Pale Violet Red
            113: "#ffefd5",  # Papaya Whip
            114: "#ffdab9",  # Peach Puff
            115: "#cd853f",  # Peru
            116: "#ffc0cb",  # Pink
            117: "#dda0dd",  # Plum
            118: "#b0e0e6",  # Powder Blue
            119: "#800080",  # Purple
            120: "#663399",  # Rebecca Purple
            121: "#ff0000",  # Red
            122: "#bc8f8f",  # Rosy Brown
            123: "#4169e1",  # Royal Blue
            124: "#8b4513",  # Saddle Brown
            125: "#fa8072",  # Salmon
            126: "#f4a460",  # Sandy Brown
            127: "#2e8b57",  # Sea Green
            128: "#fff5ee",  # Seashell
            129: "#a0522d",  # Sienna
            130: "#c0c0c0",  # Silver
            131: "#87ceeb",  # Sky Blue
            132: "#6a5acd",  # Slate Blue
            133: "#708090",  # Slate Gray
            134: "#fffafa",  # Snow
            135: "#00ff7f",  # Spring Green
            136: "#4682b4",  # Steel Blue
            137: "#d2b48c",  # Tan
            138: "#008080",  # Teal
            139: "#d8bfd8",  # Thistle
            140: "#ff6347",  # Tomato
            141: "#40e0d0",  # Turquoise
            142: "#ee82ee",  # Violet
            143: "#f5deb3",  # Wheat
            144: "#ffffff",  # White
            145: "#f5f5f5",  # White Smoke
            146: "#ffff00",  # Yellow
            147: "#9acd32",  # Yellow Green
            148: "#b0e57c",  # Inchworm
            149: "#ff6f61",  # Bittersweet
            150: "#6b4226",  # Brown Sugar
            151: "#ffcccb",  # Misty Rose
            152: "#ffebcd",  # Blanched Almond
            153: "#8a2be2",  # Blue Violet
            154: "#a52a2a",  # Brown
            155: "#deb887",  # Burly Wood
            156: "#5f9ea0",  # Cadet Blue
            157: "#7fff00",  # Chartreuse
            158: "#d2691e",  # Chocolate
            159: "#ff7f50",  # Coral
            160: "#6495ed",  # Cornflower Blue
            161: "#fff8dc",  # Cornsilk
            162: "#dc143c",  # Crimson
            163: "#00ffff",  # Cyan
            164: "#00008b",  # Dark Blue
            165: "#008b8b",  # Dark Cyan
            166: "#b8860b",  # Dark Goldenrod
            167: "#a9a9a9",  # Dark Gray
            168: "#006400",  # Dark Green
            169: "#bdb76b",  # Dark Khaki
            170: "#8b008b",  # Dark Magenta
            171: "#556b2f",  # Dark Olive Green
            172: "#ff8c00",  # Dark Orange
            173: "#9932cc",  # Dark Orchid
            174: "#8b0000",  # Dark Red
            175: "#e9967a",  # Dark Salmon
            176: "#8fbc8f",  # Dark Sea Green
            177: "#483d8b",  # Dark Slate Blue
            178: "#2f4f4f",  # Dark Slate Gray
            179: "#00ced1",  # Dark Turquoise
            180: "#9400d3",  # Dark Violet
            181: "#ff1493",  # Deep Pink
            182: "#00bfff",  # Deep Sky Blue
            183: "#696969",  # Dim Gray
            184: "#1e90ff",  # Dodger Blue
            185: "#b22222",  # Firebrick
            186: "#fffaf0",  # Floral White
            187: "#228b22",  # Forest Green
            188: "#dcdcdc",  # Gainsboro
            189: "#f8f8ff",  # Ghost White
            190: "#ffd700",  # Gold
            191: "#daa520",  # Goldenrod
            192: "#808080",  # Gray
            193: "#008000",  # Green
            194: "#adff2f",  # Green Yellow
            195: "#f0fff0",  # Honeydew
            196: "#ff69b4",  # Hot Pink
            197: "#cd5c5c",  # Indian Red
            198: "#4b0082",  # Indigo
            199: "#fffff0",  # Ivory
            200: "#f0e68c",  # Khaki
            201: "#ff6347",  # Tomato
            202: "#40e0d0",  # Turquoise
            203: "#ee82ee",  # Violet
            204: "#f5deb3",  # Wheat
            205: "#ffffff",  # White
            206: "#f5f5f5",  # White Smoke
            207: "#ffff00",  # Yellow
            208: "#9acd32",  # Yellow Green
            209: "#b0e57c",  # Inchworm
            210: "#ff6f61",  # Bittersweet
            211: "#6b4226",  # Brown Sugar
            212: "#ffcccb",  # Misty Rose
            213: "#ffebcd",  # Blanched Almond
            214: "#8a2be2",  # Blue Violet
            215: "#a52a2a",  # Brown
            216: "#deb887",  # Burly Wood
            217: "#5f9ea0",  # Cadet Blue
            218: "#7fff00",  # Chartreuse
            219: "#d2691e",  # Chocolate
            220: "#ff7f50",  # Coral
            221: "#6495ed",  # Cornflower Blue
            222: "#fff8dc",  # Cornsilk
            223: "#dc143c",  # Crimson
            224: "#00ffff",  # Cyan
            225: "#00008b",  # Dark Blue
            226: "#008b8b",  # Dark Cyan
            227: "#b8860b",  # Dark Goldenrod
            228: "#a9a9a9",  # Dark Gray
            229: "#006400",  # Dark Green
            230: "#bdb76b",  # Dark Khaki
            231: "#8b008b",  # Dark Magenta
            232: "#556b2f",  # Dark Olive Green
            233: "#ff8c00",  # Dark Orange
            234: "#9932cc",  # Dark Orchid
            235: "#8b0000",  # Dark Red
            236: "#e9967a",  # Dark Salmon
            237: "#8fbc8f",  # Dark Sea Green
            238: "#483d8b",  # Dark Slate Blue
            239: "#2f4f4f",  # Dark Slate Gray
            240: "#00ced1",  # Dark Turquoise
            241: "#9400d3",  # Dark Violet
            242: "#ff1493",  # Deep Pink
            243: "#00bfff",  # Deep Sky Blue
            244: "#696969",  # Dim Gray
            245: "#1e90ff",  # Dodger Blue
            246: "#b22222",  # Firebrick
            247: "#fffaf0",  # Floral White
            248: "#228b22",  # Forest Green
            249: "#dcdcdc",  # Gainsboro
            250: "#f8f8ff",  # Ghost White
            251: "#ffd700",  # Gold
            252: "#daa520",  # Goldenrod
            253: "#808080",  # Gray
            254: "#008000",  # Green
            255: "#adff2f",  # Green Yellow
            256: "#f0fff0",  # Honeydew
            257: "#ff69b4",  # Hot Pink
            258: "#cd5c5c",  # Indian Red
            259: "#4b0082",  # Indigo
            260: "#fffff0",  # Ivory
            261: "#f0e68c",  # Khaki
            262: "#e6e6fa",  # Lavender
            263: "#fff0f5",  # Lavender Blush
            264: "#7cfc00",  # Lawn Green
            265: "#fffacd",  # Lemon Chiffon
            266: "#add8e6",  # Light Blue
            267: "#f08080",  # Light Coral
            268: "#e0ffff",  # Light Cyan
            269: "#fafad2",  # Light Goldenrod Yellow
            270: "#d3d3d3",  # Light Gray
            271: "#ffb6c1",  # Light Pink
            272: "#ffa07a",  # Light Salmon
            273: "#20b2aa",  # Light Sea Green
            274: "#87cefa",  # Light Sky Blue
            275: "#778899",  # Light Slate Gray
            276: "#b0c4de",  # Light Steel Blue
            277: "#ffffe0",  # Light Yellow
            278: "#32cd32",  # Lime Green
            279: "#faf0e6",  # Linen
            280: "#ff00ff",  # Magenta
            281: "#800000",  # Maroon
            282: "#66cdaa",  # Medium Aquamarine
            283: "#0000cd",  # Medium Blue
            284: "#ba55d3",  # Medium Orchid
            285: "#9370db",  # Medium Purple
            286: "#3cb371",  # Medium Sea Green
            287: "#7b68ee",  # Medium Slate Blue
            288: "#00fa9a",  # Medium Spring Green
            289: "#48d1cc",  # Medium Turquoise
            290: "#c71585",  # Medium Violet Red
            291: "#191970",  # Midnight Blue
            292: "#f5fffa",  # Mint Cream
            293: "#ffe4e1",  # Misty Rose
            294: "#ffe4b5",  # Moccasin
            295: "#ffdead",  # Navajo White
            296: "#000080",  # Navy
            297: "#fdf5e6",  # Old Lace
            298: "#808000",  # Olive
            299: "#6b8e23",  # Olive Drab
            300: "#ffa500",  # Orange
            301: "#ff4500",  # Orange Red
            302: "#da70d6",  # Orchid
            303: "#eee8aa",  # Pale Goldenrod
            304: "#98fb98",  # Pale Green
            305: "#afeeee",  # Pale Turquoise
            306: "#db7093",  # Pale Violet Red
            307: "#ffefd5",  # Papaya Whip
            308: "#ffdab9",  # Peach Puff
            309: "#cd853f",  # Peru
            310: "#ffc0cb",  # Pink
            311: "#dda0dd",  # Plum
            312: "#b0e0e6",  # Powder Blue
            313: "#800080",  # Purple
            314: "#663399",  # Rebecca Purple
            315: "#ff0000",  # Red
            316: "#bc8f8f",  # Rosy Brown
            317: "#4169e1",  # Royal Blue
            318: "#8b4513",  # Saddle Brown
            319: "#fa8072",  # Salmon
            320: "#f4a460",  # Sandy Brown
            321: "#2e8b57",  # Sea Green
            322: "#fff5ee",  # Seashell
            323: "#a0522d",  # Sienna
            324: "#c0c0c0",  # Silver
            325: "#87ceeb",  # Sky Blue
            326: "#6a5acd",  # Slate Blue
            327: "#708090",  # Slate Gray
            328: "#fffafa",  # Snow
            329: "#00ff7f",  # Spring Green
            330: "#4682b4",  # Steel Blue
            331: "#d2b48c",  # Tan
            332: "#008080",  # Teal
            333: "#d8bfd8",  # Thistle
            334: "#ff6347",  # Tomato
            335: "#40e0d0",  # Turquoise
            336: "#ee82ee",  # Violet
            337: "#f5deb3",  # Wheat
            338: "#ffffff",  # White
            339: "#f5f5f5",  # White Smoke
            340: "#ffff00",  # Yellow
            341: "#9acd32",  # Yellow Green
            342: "#b0e57c",  # Inchworm
            343: "#ff6f61",  # Bittersweet
            344: "#6b4226",  # Brown Sugar
            345: "#ffcccb",  # Misty Rose
            346: "#ffebcd",  # Blanched Almond
            347: "#8a2be2",  # Blue Violet
            348: "#a52a2a",  # Brown
            349: "#deb887",  # Burly Wood
            350: "#5f9ea0",  # Cadet Blue
            351: "#7fff00",  # Chartreuse
            352: "#d2691e",  # Chocolate
            353: "#ff7f50",  # Coral
            354: "#6495ed",  # Cornflower Blue
            355: "#fff8dc",  # Cornsilk
            356: "#dc143c",  # Crimson
            357: "#00ffff",  # Cyan
            358: "#00008b",  # Dark Blue
            359: "#008b8b",  # Dark Cyan
            360: "#b8860b",  # Dark Goldenrod
            361: "#a9a9a9",  # Dark Gray
            362: "#006400",  # Dark Green
            363: "#bdb76b",  # Dark Khaki
            364: "#8b008b",  # Dark Magenta
            365: "#556b2f",  # Dark Olive Green
            366: "#ff8c00",  # Dark Orange
            367: "#9932cc",  # Dark Orchid
            368: "#8b0000",  # Dark Red
            369: "#e9967a",  # Dark Salmon
            370: "#8fbc8f",  # Dark Sea Green
            371: "#483d8b",  # Dark Slate Blue
            372: "#2f4f4f",  # Dark Slate Gray
            373: "#00ced1",  # Dark Turquoise
            374: "#9400d3",  # Dark Violet
            375: "#ff1493",  # Deep Pink
            376: "#00bfff",  # Deep Sky Blue
            377: "#696969",  # Dim Gray
            378: "#1e90ff",  # Dodger Blue
            379: "#b22222",  # Firebrick
            380: "#fffaf0",  # Floral White
            381: "#228b22",  # Forest Green
            382: "#dcdcdc",  # Gainsboro
            383: "#f8f8ff",  # Ghost White
            384: "#ffd700",  # Gold
            385: "#daa520",  # Goldenrod
            386: "#808080",  # Gray
            387: "#008000",  # Green
            388: "#adff2f",  # Green Yellow
            389: "#f0fff0",  # Honeydew
            390: "#ff69b4",  # Hot Pink
            391: "#cd5c5c",  # Indian Red
            392: "#4b0082",  # Indigo
            393: "#fffff0",  # Ivory
            394: "#f0e68c",  # Khaki
            395: "#e6e6fa",  # Lavender
            396: "#fff0f5",  # Lavender Blush
            397: "#7cfc00",  # Lawn Green
            398: "#fffacd",  # Lemon Chiffon
            399: "#add8e6",  # Light Blue
            400: "#f08080",  # Light Coral
            401: "#e0ffff",  # Light Cyan
            402: "#fafad2",  # Light Goldenrod Yellow
            403: "#d3d3d3",  # Light Gray
            404: "#ffb6c1",  # Light Pink
            405: "#ffa07a",  # Light Salmon
            406: "#20b2aa",  # Light Sea Green
            407: "#87cefa",  # Light Sky Blue
            408: "#778899",  # Light Slate Gray
            409: "#b0c4de",  # Light Steel Blue
            410: "#ffffe0",  # Light Yellow
            411: "#32cd32",  # Lime Green
            412: "#faf0e6",  # Linen
            413: "#ff00ff",  # Magenta
            414: "#800000",  # Maroon
            415: "#66cdaa",  # Medium Aquamarine
            416: "#0000cd",  # Medium Blue
            417: "#ba55d3",  # Medium Orchid
            418: "#9370db",  # Medium Purple
            419: "#3cb371",  # Medium Sea Green
            420: "#7b68ee",  # Medium Slate Blue
            421: "#00fa9a",  # Medium Spring Green
            422: "#48d1cc",  # Medium Turquoise
            423: "#c71585",  # Medium Violet Red
            424: "#191970",  # Midnight Blue
            425: "#f5fffa",  # Mint Cream
            426: "#ffe4e1",  # Misty Rose
            427: "#ffe4b5",  # Moccasin
            428: "#ffdead",  # Navajo White
            429: "#000080",  # Navy
            430: "#fdf5e6",  # Old Lace
            431: "#808000",  # Olive
            432: "#6b8e23",  # Olive Drab
            433: "#ffa500",  # Orange
            434: "#ff4500",  # Orange Red
            435: "#da70d6",  # Orchid
            436: "#eee8aa",  # Pale Goldenrod
            437: "#98fb98",  # Pale Green
            438: "#afeeee",  # Pale Turquoise
            439: "#db7093",  # Pale Violet Red
            440: "#ffefd5",  # Papaya Whip
            441: "#ffdab9",  # Peach Puff
            442: "#cd853f",  # Peru
            443: "#ffc0cb",  # Pink
            444: "#dda0dd",  # Plum
            445: "#b0e0e6",  # Powder Blue
            446: "#800080",  # Purple
            447: "#663399",  # Rebecca Purple
            448: "#ff0000",  # Red
            449: "#bc8f8f",  # Rosy Brown
            450: "#4169e1",  # Royal Blue
            451: "#8b4513",  # Saddle Brown
            452: "#fa8072",  # Salmon
            453: "#f4a460",  # Sandy Brown
            454: "#2e8b57",  # Sea Green
            455: "#fff5ee",  # Seashell
            456: "#a0522d",  # Sienna
            457: "#c0c0c0",  # Silver
            458: "#87ceeb",  # Sky Blue
            459: "#6a5acd",  # Slate Blue
            460: "#708090",  # Slate Gray
            461: "#fffafa",  # Snow
            462: "#00ff7f",  # Spring Green
            463: "#4682b4",  # Steel Blue
            464: "#d2b48c",  # Tan
            465: "#008080",  # Teal
            466: "#d8bfd8",  # Thistle
            467: "#ff6347",  # Tomato
            468: "#40e0d0",  # Turquoise
            469: "#ee82ee",  # Violet
            470: "#f5deb3",  # Wheat
            471: "#ffffff",  # White
            472: "#f5f5f5",  # White Smoke
            473: "#ffff00",  # Yellow
            474: "#9acd32",  # Yellow Green
            475: "#b0e57c",  # Inchworm
            476: "#ff6f61",  # Bittersweet
            477: "#6b4226",  # Brown Sugar
            478: "#ffcccb",  # Misty Rose
            479: "#ffebcd",  # Blanched Almond
            480: "#8a2be2",  # Blue Violet
            481: "#a52a2a",  # Brown
            482: "#deb887",  # Burly Wood
            483: "#5f9ea0",  # Cadet Blue
            484: "#7fff00",  # Chartreuse
            485: "#d2691e",  # Chocolate
            486: "#ff7f50",  # Coral
            487: "#6495ed",  # Cornflower Blue
            488: "#fff8dc",  # Cornsilk
            489: "#dc143c",  # Crimson
            490: "#00ffff",  # Cyan
            491: "#00008b",  # Dark Blue
            492: "#008b8b",  # Dark Cyan
            493: "#b8860b",  # Dark Goldenrod
            494: "#a9a9a9",  # Dark Gray
            495: "#006400",  # Dark Green
            496: "#bdb76b",  # Dark Khaki
            497: "#8b008b",  # Dark Magenta
            498: "#556b2f",  # Dark Olive Green
            499: "#ff8c00",  # Dark Orange
            500: "#9932cc",  # Dark Orchid
            501: "#e0ffff",  # Light Cyan
            502: "#fafad2",  # Light Goldenrod Yellow
            503: "#d3d3d3",  # Light Gray
            504: "#ffb6c1",  # Light Pink
            505: "#ffa07a",  # Light Salmon
            506: "#20b2aa",  # Light Sea Green
            507: "#87cefa",  # Light Sky Blue
            508: "#778899",  # Light Slate Gray
            509: "#b0c4de",  # Light Steel Blue
            510: "#ffffe0",  # Light Yellow
            511: "#32cd32",  # Lime Green
            512: "#faf0e6",  # Linen
            513: "#ff00ff",  # Magenta
            514: "#800000",  # Maroon
            515: "#66cdaa",  # Medium Aquamarine
            516: "#0000cd",  # Medium Blue
            517: "#ba55d3",  # Medium Orchid
            518: "#9370db",  # Medium Purple
            519: "#3cb371",  # Medium Sea Green
            520: "#7b68ee",  # Medium Slate Blue
            521: "#00fa9a",  # Medium Spring Green
            522: "#48d1cc",  # Medium Turquoise
            523: "#c71585",  # Medium Violet Red
            524: "#191970",  # Midnight Blue
            525: "#f5fffa",  # Mint Cream
            526: "#ffe4e1",  # Misty Rose
            527: "#ffe4b5",  # Moccasin
            528: "#ffdead",  # Navajo White
            529: "#000080",  # Navy
            530: "#fdf5e6",  # Old Lace
            531: "#808000",  # Olive
            532: "#6b8e23",  # Olive Drab
            533: "#ffa500",  # Orange
            534: "#ff4500",  # Orange Red
            535: "#da70d6",  # Orchid
            536: "#eee8aa",  # Pale Goldenrod
            537: "#98fb98",  # Pale Green
            538: "#afeeee",  # Pale Turquoise
            539: "#db7093",  # Pale Violet Red
            540: "#ffefd5",  # Papaya Whip
            541: "#ffdab9",  # Peach Puff
            542: "#cd853f",  # Peru
            543: "#ffc0cb",  # Pink
            544: "#dda0dd",  # Plum
            545: "#b0e0e6",  # Powder Blue
            546: "#800080",  # Purple
            547: "#663399",  # Rebecca Purple
            548: "#ff0000",  # Red
            549: "#bc8f8f",  # Rosy Brown
            550: "#4169e1",  # Royal Blue
            551: "#8b4513",  # Saddle Brown
            552: "#fa8072",  # Salmon
            553: "#f4a460",  # Sandy Brown
            554: "#2e8b57",  # Sea Green
            555: "#fff5ee",  # Seashell
            556: "#a0522d",  # Sienna
            557: "#c0c0c0",  # Silver
            558: "#87ceeb",  # Sky Blue
            559: "#6a5acd",  # Slate Blue
            560: "#708090",  # Slate Gray
            561: "#fffafa",  # Snow
            562: "#00ff7f",  # Spring Green
            563: "#4682b4",  # Steel Blue
            564: "#d2b48c",  # Tan
            565: "#008080",  # Teal
            566: "#d8bfd8",  # Thistle
            567: "#ff6347",  # Tomato
            568: "#40e0d0",  # Turquoise
            569: "#ee82ee",  # Violet
            570: "#f5deb3",  # Wheat
            571: "#ffffff",  # White
            572: "#f5f5f5",  # White Smoke
            573: "#ffff00",  # Yellow
            574: "#9acd32",  # Yellow Green
            575: "#b0e57c",  # Inchworm
            576: "#ff6f61",  # Bittersweet
            577: "#6b4226",  # Brown Sugar
            578: "#ffcccb",  # Misty Rose
            579: "#ffebcd",  # Blanched Almond
            580: "#8a2be2",  # Blue Violet
            581: "#a52a2a",  # Brown
            582: "#deb887",  # Burly Wood
            583: "#5f9ea0",  # Cadet Blue
            584: "#7fff00",  # Chartreuse
            585: "#d2691e",  # Chocolate
            586: "#ff7f50",  # Coral
            587: "#6495ed",  # Cornflower Blue
            588: "#fff8dc",  # Cornsilk
            589: "#dc143c",  # Crimson
            590: "#00ffff",  # Cyan
            591: "#00008b",  # Dark Blue
            592: "#008b8b",  # Dark Cyan
            593: "#b8860b",  # Dark Goldenrod
            594: "#a9a9a9",  # Dark Gray
            595: "#006400",  # Dark Green
            596: "#bdb76b",  # Dark Khaki
            597: "#8b008b",  # Dark Magenta
            598: "#556b2f",  # Dark Olive Green
            599: "#ff8c00",  # Dark Orange
            600: "#9932cc",  # Dark Orchid
        }

        file_path = "solution.html"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("<html><head><style>table {border-collapse: collapse;} td {border: 1px solid black; width: 40px; height: 40px; text-align: center;}</style></head><body><table>")
            for r in range(solution_grid.rows_number):
                file.write("<tr>")
                for c in range(solution_grid.columns_number):
                    inner_text = '■' if solution_grid.value(r, c) is True else ''
                    background_color = color_map.get(grid.value(r, c))
                    file.write(f"<td style='background-color: {background_color};'>{inner_text}</td>")
                file.write("</tr>")
            file.write("</table></body></html>")
        webbrowser.open(file_path)


if __name__ == '__main__':
    NorinoriMainConsole.main()
