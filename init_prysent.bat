DEL database\db.sqlite3

CALL activate prysent2204

python .\src\manage.py migrate --settings=prysent.settings.prod
python .\src\manage.py auto_create_superuser --settings=prysent.settings.prod
python .\src\manage.py upload_media --settings=prysent.settings.prod