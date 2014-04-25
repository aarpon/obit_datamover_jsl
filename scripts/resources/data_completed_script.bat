@echo off

REM Call the dataCompletedScript executable pasing the parameter received from Datamover
%~dp0\data_completed\dataCompletedScript.exe %1

REM Return the exit value of dataCompletedScript to Datamover
exit %ERRORLEVEL%
