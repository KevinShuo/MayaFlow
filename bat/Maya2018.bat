@echo off
set "XBMLANGPATH=%~dp0../resources"
set "SCRIPTS_PATH=%~dp0../scripts"
set "CGTM=C:\CgTeamWork_v7\bin\base"
set "SRC_PATH=%~dp0../src/py2/abc"
set "INFO_METHOD=file"
set "PIPELINE_TYPE=abc"
set "PYTHONPATH=C:\dev\maya\MayaFlow;C:\dev\maya\MayaFlow\scripts;C:\dev\maya\MayaFlow\libs\py2\site-packages;%CGTM%;%SRC_PATH%;%PYTHONPATH%"

"C:\Program Files\Autodesk\Maya2018\bin\maya.exe"