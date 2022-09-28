CALL activate prysent2204

date /t >> c:\PythonApps\prysent\logs\prysent.log
time /t >> c:\PythonApps\prysent\logs\prysent.log

python c:\PythonApps\prysent\src\manage.py upload_schedule --settings=prysent.settings.prod >> c:\PythonApps\prysent\logs\prysent.log