# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             binaries=[('.\\sdk\\lib\\curve_analysis_platform.dll', 'sdk\\lib\\.'),
                       ('.\\sdk\\lib\\libcurve_analysis_platform.so', 'sdk\\lib\\.')],
             datas=[('.\\datasets', 'pyecharts\\datasets\\.'),
                    ('.\\templates', 'templates\\.')],
             hiddenimports=["jsoncomparison"],
             hookspath=[],
             runtime_hooks=['package_runtime.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='toolkit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='toolkit')
