CALL activate prysent2204

date /t >> c:\PythonApps\present\logs\run_schedule.log
time /t >> c:\PythonApps\present\logs\run_schedule.log

python c:\PythonApps\present\src\manage.py run_schedule --settings=prysent.settings.prod >> c:\PythonApps\present\logs\run_schedule.log