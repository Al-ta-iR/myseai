@echo off

:loop
tasklist | find /i "bot_ai_search.exe" > nul
if errorlevel 1 (
    start /B D:\Dev\myseai\dist\bot_ai_search.exe
)

timeout /t 60 > nul
goto loop
