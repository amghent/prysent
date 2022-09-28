CALL activate prysent2204

date /t >> c:\PythonApps\prysent\logs\prysent.log
time /t >> c:\PythonApps\prysent\logs\prysent.log

python c:\PythonApps\prysent\src\manage.py remove_cached_notebooks --settings=prysent.settings.prod >> c:\PythonApps\prysent\logs\prysent.log