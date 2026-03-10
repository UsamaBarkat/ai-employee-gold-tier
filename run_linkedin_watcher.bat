@echo off
REM LinkedIn Watcher - Automated Run
REM Part of Silver Tier - Personal AI Employee Hackathon

cd /d "E:\AI-300\My_Hackathons_Teacher"
python linkedin_watcher.py --auto

REM If there's an error, log it
if errorlevel 1 (
    echo Error occurred at %date% %time% >> linkedin_watcher_errors.log
)
