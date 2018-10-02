pyinstaller -F -w ui\settings.py
pyinstaller -F -w --hidden-import=win32timezone service\poc_service.py
pyinstaller -F -w prepenv.py
"%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe" installer.iss