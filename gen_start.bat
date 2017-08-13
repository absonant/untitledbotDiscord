:: Use this to generate a start file with required env vars

title untitledbot Generation Script
@echo off

:main
cls
echo Generate a start.bat file for untitledbot
echo Press any key to start
pause >nul

:token
cls
echo Right-click and paste your Discord API token.
set /p discordapitoken=
echo Saved
timeout /t 2 /nobreak >nul

:debugmode
cls
echo Type 1 to run untitledbot in debugmode, or 0 to run in production.
set /p debugmode=
echo Saved
timeout /t 2 /nobreak >nul

:write
cls
echo Saving to file...
echo title untitledbot >start.bat
echo @echo off >>start.bat
echo cls >>start.bat
echo set DISCORD_UB_TOKEN=%discordapitoken% >>start.bat
echo if debugmode==1 set DISCORD_UB_DEBUG=NOTABLANKVALUE >>start.bat
:: todo test above
echo Done. Press any key to exit
pause >nul
exit