import math
import re
import sys
import time

def is_perfect_square(n):
    if n < 0:
        return False
    sqrt_n = math.sqrt(n)
    return sqrt_n.is_integer()


def clean_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def custom_tqdm(iterable, desc="", unit="it", total=None):
    if total is None:
        total = len(iterable)
    start_time = time.time()

    def print_progress(iteration):
        elapsed_time = time.time() - start_time
        progress = (iteration + 1) / total
        bar_length = 40
        block = int(round(bar_length * progress))
        text = f"\r{desc} [{'#' * block + '-' * (bar_length - block)}] {iteration + 1}/{total} {unit} ({elapsed_time:.2f}s)"
        sys.stdout.write(text)
        sys.stdout.flush()

    for i, item in enumerate(iterable):
        yield item
        print_progress(i)
    sys.stdout.write("\n")
    sys.stdout.flush()
