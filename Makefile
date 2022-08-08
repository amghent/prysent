init-once:
	mkdir ./database

	mkdir -p ./src
	django-admin startproject prysent ./src/

	mkdir -p ./src/dashboard
	django-admin startapp dashboard ./src/dashboard

	mkdir -p ./src/_templates/default
	mkdir -p ./src/_bootstrap/management/commands

migrate:
	python src/manage.py makemigrations
	python src/manage.py migrate

delete-db:
	rm -f ./database/db.sqlite3

superuser:
	python src/manage.py auto_create_superuser

sample-data:
	python src/manage.py sample_data

reset-db: delete-db migrate superuser sample-data

run: migrate
	python ./src/manage.py runserver

test:
	python ./src/manage.py test

voila:
	voila ./media --port=8876 --no-browser --Voila.tornado_settings="{'headers':{'Content-Security-Policy': 'frame-ancestors http://127.0.0.1:8000'}}" &
