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

reset-db: delete-db migrate superuser

run: migrate
	python ./src/manage.py runserver

test:
	python ./src/manage.py test
