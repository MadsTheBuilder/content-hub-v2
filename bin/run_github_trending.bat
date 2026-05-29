@echo off
:: Daily GitHub trending AI repos script
:: Schedule via Windows Task Scheduler — daily at 08:00
::
:: Task Scheduler setup:
::   Program/script: C:\Users\madhu\Claude cowork\Content Hub V2\bin\run_github_trending.bat
::   Start in:       C:\Users\madhu\Claude cowork\Content Hub V2
::   Trigger:        Daily, 08:00 AM
::   Condition:      Start only if network is available

cd /d "C:\Users\madhu\Claude cowork\Content Hub V2"
python scripts\github_trending.py >> logs\github_trending.log 2>&1
