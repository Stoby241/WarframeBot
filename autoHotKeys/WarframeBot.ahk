#MaxThreadsPerHotkey 3

#::
IfWinNotExist, ahk_exe cmd.exe
{
run cmd.exe	
WinWait, ahk_exe cmd.exe ; Wait for CMD to start
}
WinActivate C:\WINDOWS\SYSTEM32\cmd.exe
Send H:{enter} ; Go to C drive
Send cd H:\dev\WarframeBot{enter}
Send venv\Scripts\python.exe lookUpIRelictPrice.py{enter}
return



