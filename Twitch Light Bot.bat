@ECHO OFF
ECHO Starting BlueStacks.exe
START C:\"Program Files"\BlueStacks_nxt\HD-Player.exe --instance Nougat32 ::or wherever Bluestacks is installed
timeout /t 10 /nobreak

SET /A attempts=1
ECHO Starting ADB Server
:loop
adb start-server

::ECHO Switching PC lights to streamer profile
::wscript //NoLogo "C:\Users\dylan\Documents\GitHub\govee-stream-controller\keys.vbs"

C:\Users\dylan\.virtualenvs\govee-stream-controller-lXkerzrS\Scripts\python.exe C:\Users\dylan\Documents\GitHub\govee-stream-controller\bot.py || find "No Devices"
IF not errorlevel 1 (
	SET /A attempts=%attempts%+1
	IF %attempts% lss 5 (
		ECHO Failed to initialize, restarting ADB Server
		adb kill-server 
		goto :loop ) ELSE (ECHO Timeout reached: Failed to initialize)
)
PAUSE


