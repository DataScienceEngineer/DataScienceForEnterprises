set mypath=%cd%
sphinx-build %mypath%\docs\source %mypath%\docs\html
cd tests
python -m pytest -v -s
cmd