set mypath=%cd%
sphinx-build %mypath%\docs\source %mypath%\docs\html
start iexplore.exe %mypath%\docs\html\index.html
pause
cmd