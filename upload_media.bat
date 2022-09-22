CALL activate prysent2204

date /t >> c:\PythonApps\present\logs\upload_media.log
time /t >> c:\PythonApps\present\logs\upload_media.log

python c:\PythonApps\present\src\manage.py upload_media --settings=prysent.settings.prod >> c:\PythonApps\present\logs\upload_media.log