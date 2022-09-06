/quiet InstallAllUsers=1 PrependPath=1 Include_test=0

@REM @echo off

set python_loc=%cd%\bin\


cd %python_loc%

python-2.7.18.msi /quiet InstallAllUsers=0 PrependPath=1 Include_test=0


pip install portablemc

pip install portablemc-forge

pip install PyQt5

pip install wget