# main.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('config/saved_colors.csv', 'config'),
        ('config/selected_colors.csv', 'config'),
        ('config/settings.json', 'config'),
        ('assets/color_converter_dark.png', 'assets'),
        ('assets/color_converter_light.png', 'assets'),
        ('assets/color_gear_dark.png', 'assets'),
        ('assets/color_gear_light.png', 'assets'),
        ('assets/color_grab_dark.png', 'assets'),
        ('assets/color_grab_light.png', 'assets'),
        ('assets/icon.ico', 'assets'),
        ('assets/ncm_app_dark.png', 'assets'),
        ('assets/ncm_app_light.png', 'assets'),
        ('assets/settings.png', 'assets'),
        ('assets/tutorials.png', 'assets')
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'customtkinter',
        'tkinter',
        'json',
        'os',
        'ctypes',
        'webbrowser',
        'PIL',
        'numpy',
        'sklearn.cluster',
        'colorthief',
        'csv',
        'atexit',
        'cv2',
        'pyperclip'
    ],
    hookspath=[],
    runtime_hooks=[],
    exludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)