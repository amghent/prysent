init-once:
	mkdir -p ./src
	django-admin startproject prysent ./src/

	mkdir -p ./src/dashboard
	django-admin startapp dashboard ./src/dashboard

	mkdir -p ./src/_templates/default

migrate:
	python src/manage.py makemigrations
	python src/manage.py migrate

run:
	python ./src/manage.py runserver

test:
	python ./src/manage.py test
