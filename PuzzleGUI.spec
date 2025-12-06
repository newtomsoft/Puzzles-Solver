# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all submodules for complex packages
hiddenimports = [
    'tkinter',
    'tkinter.scrolledtext',
    'tkinter.messagebox',
    'playwright',
    'playwright.sync_api',
    'z3',
    'ortools',
    'ortools.sat',
    'ortools.sat.python',
    'ortools.sat.python.cp_model',
    'moviepy',
    'moviepy.editor',
    'imageio',
    'imageio.core',
    'imageio.plugins',
    'imageio_ffmpeg',
    'bs4',
    'beautifulsoup4',
    'requests',
    'configparser',
    'numpy',
    'bitarray',
    'tqdm',
    'flask',
    'flask_cors',
]

# Collect data files
from PyInstaller.utils.hooks import copy_metadata

datas = [
    ('GridProviders/ScrapingGridProvider.ini', 'GridProviders'),
    ('GridProviders/Chromium', 'GridProviders/Chromium'),
    ('GridProviders/Firefox', 'GridProviders/Firefox'),
]

# Collect metadata for packages that need it (using copy_metadata for importlib.metadata support)
datas += copy_metadata('imageio')
datas += copy_metadata('imageio_ffmpeg')

# Collect binaries for Z3 and OR-Tools (native libraries)
import z3
import ortools
import glob
z3_path = os.path.dirname(z3.__file__)
ortools_path = os.path.dirname(ortools.__file__)

binaries = []

# Z3 binaries
z3_lib_dir = os.path.join(z3_path, 'lib')
if os.path.exists(z3_lib_dir):
    for dll in glob.glob(os.path.join(z3_lib_dir, '*.dll')):
        binaries.append((dll, 'z3/lib'))
    for so in glob.glob(os.path.join(z3_lib_dir, '*.so*')):
        binaries.append((so, 'z3/lib'))

# Z3 root directory binaries
for dll in glob.glob(os.path.join(z3_path, '*.dll')):
    binaries.append((dll, 'z3'))

# OR-Tools binaries
ortools_libs_dir = os.path.join(ortools_path, '.libs')
if os.path.exists(ortools_libs_dir):
    for dll in glob.glob(os.path.join(ortools_libs_dir, '*.dll')):
        binaries.append((dll, 'ortools/.libs'))
    for so in glob.glob(os.path.join(ortools_libs_dir, '*.so*')):
        binaries.append((so, 'ortools/.libs'))

# Add all Python packages from the project
a = Analysis(
    ['Run/PuzzleGUI.py'],
    pathex=['G:\\projets infos\\PuzzleGames'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

splash = Splash(
    'games.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='PuzzleSolver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PuzzleSolver',
)
