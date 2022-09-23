DEL c:\PythonApps\prysent\database\db.sqlite3

CALL activate prysent2204

python c:\PythonApps\prysent\src\manage.py migrate --settings=prysent.settings.prod
python c:\PythonApps\prysent\src\manage.py auto_create_superuser --settings=prysent.settings.prod
python c:\PythonApps\prysent\src\manage.py clean_cache --settings=prysent.settings.prod
python c:\PythonApps\prysent\src\manage.py upload_media --settings=prysent.settings.prod
python c:\PythonApps\prysent\src\manage.py upload_schedule --settings=prysent.settings.prod
