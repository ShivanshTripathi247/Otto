# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(['main.py'],
             pathex=['D:\\otto'], # The path to your project
             binaries=[],
             datas=[
                 ('assets', 'assets'),
                 ('ui_manager.py', '.'),
                 ('sentinel_core.py', '.'),
                 ('speaker.py', '.'),
                 ('listener.py', '.'),
                 ('llm_handler.py', '.'),
                 ('dashboard_ui.py', '.'),
                 ('calendar_handler.py', '.'),
                 ('api_handler.py', '.'),
                 ('config.json', '.'),
                 ('credentials.json', '.')
             ],
             hiddenimports=['pystray._win32'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Otto',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False, # Set to False to hide the terminal window
          icon='assets\\icon.ico') # You need an .ico file for the executable