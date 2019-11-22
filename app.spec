# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\utilisateur\\Dropbox\\Hobbies\\slothplayer'],
             binaries=[],
             datas=[('./libvlc.dll', '.'), ('./axvlc.dll', '.'), ('./libvlccore.dll', '.'), ('./npvlc.dll', '.'), ('./config.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('C:\Program Files\VideoLAN\VLC\plugins', prefix='plugins')
a.datas += Tree('C:\Program Files\VideoLAN\VLC\lua', prefix='lua')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='slothplayer',
          icon='icon.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='slothplayer')

#import shutil
#shutil.copyfile('config.txt', '{0}/config.txt'.format(DISTPATH))
