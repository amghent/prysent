CALL activate prysent2204

date /t >> c:\PythonApps\present\logs\prysent.log
time /t >> c:\PythonApps\present\logs\prysent.log

python c:\PythonApps\present\src\manage.py runserver 0.0.0.0:8875 --settings=prysent.settings.prod >> c:\PythonApps\present\logs\prysent.log