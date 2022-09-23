CALL activate prysent2204

date /t >> c:\PythonApps\prysent\logs\prysent.log
time /t >> c:\PythonApps\prysent\logs\prysent.log

python c:\PythonApps\prysent\src\manage.py runserver 0.0.0.0:8875 --settings=prysent.settings.prod >> c:\PythonApps\prysent\logs\prysent.log