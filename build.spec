# build.spec
import os
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Use sys.argv[0] to get the current script's directory
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Define the path to your assets folder
assets_dir = os.path.join(current_dir, 'assets')

# Recursively collect all files in the assets directory.
# For each file, the target will be placed under an "assets" folder in the bundle.
datas = []
for root, dirs, files in os.walk(assets_dir):
    for file in files:
        full_path = os.path.join(root, file)
        # Calculate the relative path with respect to the assets folder.
        rel_path = os.path.relpath(full_path, assets_dir)
        # The target folder in the bundle will be "assets/rel_path"
        datas.append((full_path, os.path.join('assets', rel_path)))

# Also add the database file from src.
datas.append(('src/password_history.db', '.'))

a = Analysis(
    ['src/main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PasswordChecker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
