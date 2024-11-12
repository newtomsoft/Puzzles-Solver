import re


def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


console_back_ground_colors = {
    0: "\033[40m",  # Black background
    1: "\033[107m",  # White background
    2: "\033[43m",  # Yellow background
    3: "\033[44m",  # Blue background
    4: "\033[45m",  # Magenta background
    5: "\033[48;5;164m",  # Light blue background
    6: "\033[42m",  # Green background
    7: "\033[48;5;162m",  # Pink background
    8: "\033[101m",  # Light red background
    9: "\033[102m",  # Light green background
    10: "\033[103m",  # Light yellow background
    11: "\033[105m",  # Light magenta background
    12: "\033[48;5;208m",  # Orange background
    13: "\033[48;5;226m",  # Light yellow background
    14: "\033[48;5;27m",  # Light blue background
    15: "\033[48;5;160m",  # Red background
    16: "\033[41m",  # Red background
    17: "\033[107m",  # Light grey background
    18: "\033[46m",  # Cyan background
    19: "\033[48;5;165m",  # Light magenta background
    20: "\033[48;5;166m",  # Light orange background
    21: "\033[48;5;167m",  # Light yellow background
    22: "\033[48;5;168m",  # Light green background
    'end': '\033[0m',  # Reset
}

console_police_colors = {
    0: "\033[95m",  # Magenta light
    1: "\033[93m",  # Yellow light
    2: "\033[96m",  # Cyan light
    3: "\033[92m",  # Green light
    4: "\033[97m",  # White
    5: "\033[91m",  # Red light
    6: "\033[32m",  # Green
    7: "\033[90m",  # Grey
    8: "\033[35m",  # Magenta
    9: "\033[36m",  # Cyan
    10: "\033[34m",  # Blue
    11: "\033[31m",  # Red
    12: "\033[33m",  # Yellow
    13: "\033[94m",  # Blue light
    14: "\033[38;5;208m",  # Orange
    15: "\033[38;5;226m",  # Light yellow
    16: "\033[30m",  # Black
    'end': '\033[0m',
}
