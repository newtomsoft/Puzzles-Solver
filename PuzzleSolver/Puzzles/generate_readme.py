#!/usr/bin/env python3
"""Generate README.md for each puzzle folder with French rules from gridpuzzle.com."""
import os
import re
import time
import urllib.request
import urllib.error
import html.parser
PUZZLES_DIR = os.path.dirname(os.path.abspath(__file__))
EXCLUDE = {"__pycache__", "GameSolver.py", "utils.py", "generate_readme.py"}
SLUG_MAP = {
    "Akari": "lightup",
    "Aqre": "aqre",
    "Araf": "araf",
    "Arofuro": "arofuro",
    "ArrowWeb": "arrow-web",
    "ArukoneNo2x2": "arukone-no-2x2",
    "BalanceLoop": "balance-loop",
    "BorderBlock": "bodaburokku",
    "Buraitoraito": "bright-light",
    "Chocona": "chocona",
    "CirclesAndSquares": "circles-and-squares",
    "Clouds": "clouds",
    "CornerLoop": "konarupu",
    "Corral": "cave",
    "CountryRoad": "country-road",
    "Creek": "creek",
    "Deddoanguru": "deddoanguru",
    "Detour": "detour",
    "Doppelblock": "doppelblock",
    "DosunFuwari": "dosun-fuwari",
    "DotchiLoop": "dotchiloop",
    "DoubleMinesweeper": "minesweeper-double",
    "EverySecondTurn": "every-second-turn",
    "Factorism": "factorism",
    "Fobidoshi": "fobidoshi",
    "From1ToX": "from1tox",
    "Gappy": "gappy",
    "Geradeweg": "straight-loop",
    "Grades": "grades",
    "GrandTour": "grandtour",
    "Gyokuseki": "gyokuseki",
    "Hakoiri": "hakoiri",
    "Hanare": "hanare",
    "Hashi": "bridges",
    "Hiroimono": "hiroimono",
    "Ichimaga": "ichimaga",
    "Irasuto": "irasuto",
    "Island": "island",
    "KakuteruAnpu": "cocktail-lamp",
    "Kanjo": "kanjo",
    "Kazoku": "kazoku",
    "KinKonKan": "kin-kon-kan",
    "Knossos": "knossos",
    "Koburin": "koburin",
    "KohiGyunyu": "kohi-gyunyu",
    "Konarupu": "konarupu",
    "Kuroshiro": "kuroshiro",
    "Kuroshuto": "kuroshuto",
    "Kurotto": "kurotto",
    "Linesweeper": "linesweeper",
    "LookAir": "look-air",
    "Masyu": "masyu",
    "Mathrax": "mathrax",
    "Meadows": "meadows",
    "MidLoop": "mid-loop",
    "Minesweeper": "minesweeper",
    "Mintonette": "mintonette",
    "Mirukuti": "mirukuti",
    "Miti": "miti",
    "Mobiriti": "mobiriti",
    "Moonsun": "moonsun",
    "Nanro": "nanro",
    "Neighbours": "neighbours",
    "No4InARow": "no-four-in-row",
    "NumberChain": "number-chain",
    "NumberCross": "number-cross",
    "NumberLink": "arukone",
    "Nuribou": "nuribou",
    "Obitaru": "obitaru",
    "Pipelink": "pipelink",
    "Purenrupu": "pure-loop",
    "RabbitsAndTrees": "rabbits-and-trees",
    "RegionalYajilin": "regional-yajilin",
    "Renkatsu": "renkatsu",
    "RoundTrip": "round-trip",
    "Sashikazune": "sashikazune",
    "SeeThrough": "seethrough",
    "SheepAndWolves": "sheep-and-wolves",
    "Shimaguni": "shimaguni",
    "Shingoki": "traffic-lights",
    "Shirokuro": "shirokuro",
    "Slitherlink": "slitherlink",
    "Snake": "snake",
    "StarBattle": "starbattle",
    "StarsAndArrows": "stars-and-arrows",
    "Str8ts": "str8ts",
    "Summandum": "summandum",
    "Suriza": "slitherlink",
    "Sutoreto": "sutoreto",
    "Tapa": "tapa",
    "Tasukuea": "tasukuea",
    "Tatamibari": "tatamibari",
    "TentaiShow": "galaxies",
    "TilePaint": "tilepaint",
    "Toichika": "toichika",
    "Trilogy": "trilogy",
    "Usotatami": "usotatami",
    "Usowan": "usowan",
    "Wamuzu": "wamuzu",
    "Yajikabe": "yajikabe",
    "Yajilin": "yajilin",
    "Yonmasu": "yonmasu",
}
class RuleExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self._capture = False
        self._in_h1 = False
        self._h1_done = False
        self._depth = 0
        self._parts = []
        self._current_text = []
        self._skip_tags = {"script", "style", "nav", "header", "footer", "aside", "noscript"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._depth += 1
            return
        if tag == "h1" and not self._h1_done:
            self._in_h1 = True
        if self._capture and tag in ("br", "p", "div", "h2", "h3", "li", "ul", "ol"):
            self._flush_text()

    def handle_endtag(self, tag):
        if tag in self._skip_tags and self._depth > 0:
            self._depth -= 1
            return
        if tag == "h1" and self._in_h1:
            self._in_h1 = False
            self._h1_done = True
            self._capture = True
            self._flush_text()
        if self._capture and tag in ("p", "div", "h2", "h3", "li"):
            self._flush_text()

    def handle_data(self, data):
        if self._depth > 0:
            return
        if self._in_h1 or self._capture:
            text = data.strip()
            if text:
                self._current_text.append(text)

    def _flush_text(self):
        if self._current_text:
            line = " ".join(self._current_text)
            # Clean up bold markers and extra spaces
            line = re.sub(r'\*+', '', line)
            line = re.sub(r'\s+', ' ', line).strip()
            if line:
                self._parts.append(line)
            self._current_text = []

    def get_rules(self):
        self._flush_text()
        rules = []
        stop_keywords = [
            "jouer maintenant", "play now", "copier", "copy & share",
            "puzzles recommandés", "recommended puzzles",
            "inscrire", "connexion", "accueil", "home",
            "sudoku puzzles", "logic puzzles", "puzzles logiques",
        ]
        for line in self._parts:
            if not line:
                continue
            if len(line) < 10:
                continue
            if any(line.lower().startswith(kw) for kw in stop_keywords):
                break
            rules.append(line)
        return rules

def fetch_url(url, max_retries=3):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; PuzzleBot; +https://github.com/anomalyco/PuzzleGames)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            if attempt == max_retries - 1:
                return None
            time.sleep(1)
    return None

def get_slug(folder_name):
    if folder_name in SLUG_MAP:
        return SLUG_MAP[folder_name]
    return folder_name.lower()

def is_homepage(html):
    lowercase = html.lower()
    nav_home = 'entraînez votre cerveau' in lowercase or 'train your brain' in lowercase
    nav_home = nav_home or ('daily challenges' in lowercase and 'leaderboards' in lowercase)
    return nav_home and 'class="rule"' not in lowercase and 'rules & tips' not in lowercase and 'règles et astuces' not in lowercase

def extract_rules_from_html(html):
    parser = RuleExtractor()
    parser.feed(html)
    return parser.get_rules()

def find_urls_in_test_files(folder_path):
    urls = []
    test_dir = os.path.join(folder_path, "tests")
    if os.path.isdir(test_dir):
        for fname in os.listdir(test_dir):
            if fname.endswith(".py"):
                fpath = os.path.join(test_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                found = re.findall(r'https?://[^\s"\'\]()<>]+', content)
                urls.extend(found)
    # Also check solver file
    solver_name = os.path.basename(folder_path)
    solver_file = os.path.join(folder_path, f"{solver_name}Solver.py")
    if os.path.exists(solver_file):
        with open(solver_file, "r", encoding="utf-8") as f:
            content = f.read()
        found = re.findall(r'https?://[^\s"\'\]()<>]+', content)
        urls.extend(found)
    return urls

def format_rules_text(rules_lines, puzzle_name):
    lines = [f"# {puzzle_name}", "", "## Règles du jeu", ""]
    for line in rules_lines:
        lines.append(line)
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    lines.append("")
    return "\n".join(lines)

def main():
    puzzles = sorted(
        f
        for f in os.listdir(PUZZLES_DIR)
        if f not in EXCLUDE and os.path.isdir(os.path.join(PUZZLES_DIR, f))
    )
    print(f"Found {len(puzzles)} puzzle directories")
    skipped = []
    success = []
    failed = []
    for folder_name in puzzles:
        folder_path = os.path.join(PUZZLES_DIR, folder_name)
        readme_path = os.path.join(folder_path, "README.md")
        if os.path.exists(readme_path):
            print(f"  SKIP  {folder_name} (README.md already exists)")
            skipped.append(folder_name)
            continue
        slug = get_slug(folder_name)
        french_url = f"https://fr.gridpuzzle.com/{slug}/rule"
        english_url = f"https://gridpuzzle.com/{slug}/rule"
        print(f"  FETCH {folder_name} -> {french_url}")
        html = fetch_url(french_url)
        # If French returns homepage, try English
        if html and is_homepage(html):
            print(f"    -> French is homepage, trying English: {english_url}")
            html = fetch_url(english_url)
        if html is None:
            print(f"    FAIL {folder_name}: cannot fetch any rule page")
            failed.append(folder_name)
            continue
        rules = extract_rules_from_html(html)
        # If still homepage or no rules, try extracting slug from test files
        if is_homepage(html) or not rules:
            alt_urls = find_urls_in_test_files(folder_path)
            for alt_url in alt_urls:
                if "gridpuzzle.com" in alt_url and "/rule" not in alt_url:
                    # Try to get the rule page from this puzzle's URL
                    match = re.match(r'https?://[^/]+/([^/]+)', alt_url)
                    if match:
                        alt_slug = match.group(1)
                        alt_rule_url = f"https://fr.gridpuzzle.com/{alt_slug}/rule"
                        print(f"    -> trying slug from test: {alt_rule_url}")
                        html2 = fetch_url(alt_rule_url)
                        if html2 and not is_homepage(html2):
                            rules = extract_rules_from_html(html2)
                            if rules:
                                break
                        # Try English
                        alt_rule_url_en = f"https://gridpuzzle.com/{alt_slug}/rule"
                        html2 = fetch_url(alt_rule_url_en)
                        if html2 and not is_homepage(html2):
                            rules = extract_rules_from_html(html2)
                            if rules:
                                break
        if not rules:
            print(f"    FAIL {folder_name}: no rules extracted")
            failed.append(folder_name)
            continue
        readme_content = format_rules_text(rules, folder_name)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        print(f"    OK   {folder_name} ({len(rules)} lines)")
        success.append(folder_name)
        time.sleep(0.3)
    print()
    print("=== Summary ===")
    print(f"Success: {len(success)}")
    print(f"Skipped (already exists): {len(skipped)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(f"Failed puzzles: {', '.join(failed)}")


if __name__ == "__main__":
    main()