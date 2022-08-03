init-once:
	mkdir -p ./src
	django-admin startproject prysent ./src/

	mkdir -p ./src/dashboard
	django-admin startapp dashboard ./src/dashboard

run:
	python ./src/manage.py runserver

test:
	python ./src/manage.py test
