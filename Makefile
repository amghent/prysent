SHELL := /bin/bash
MS_SQLCMD := /opt/mssql-tools/bin/sqlcmd

init-once:
	mkdir ./database

	mkdir -p ./src
	django-admin startproject prysent ./src/

	mkdir -p ./src/dashboard
	django-admin startapp dashboard ./src/dashboard
	mkdir -p ./src/_world_api
	django-admin startapp _world_api ./src/_world_api

	mkdir -p ./src/_templates/default
	mkdir -p ./src/_bootstrap/management/commands

validate:
ifndef SETTINGS
	@echo "Specify SETTINGS to set the environment"
	@exit 1
endif

login: validate
ifeq ("$(SETTINGS)", "prysent.settings.mssql")
	source ./src/_bootstrap/management/config/mssql/sa.secret && \
	$(MS_SQLCMD) -S localhost -C -U sa -P "$(MSSQL_SA_PASSWORD)" -i ./src/_bootstrap/management/sql/mssql/drop_login.sql  && \
	$(MS_SQLCMD) -S localhost -C -U sa -P "$(MSSQL_SA_PASSWORD)" -i ./src/_bootstrap/management/sql/mssql/create_login.sql
endif

create-db: validate
ifeq ("$(SETTINGS)", "prysent.settings.sqlite3")
	rm -rf ./database/db.sqlite3
endif

ifeq ("$(SETTINGS)", "prysent.settings.postgres")
	sudo -u postgres psql -d postgres -f src/_bootstrap/management/sql/postgres/create_db.sql ;
endif

ifeq ("$(SETTINGS)", "prysent.settings.mssql")
	source ./src/_bootstrap/management/config/mssql/sa.secret && \
	$(MS_SQLCMD) -S localhost -C -U sa -P "$(MSSQL_SA_PASSWORD)" -i ./src/_bootstrap/management/sql/mssql/drop_db.sql && \
	$(MS_SQLCMD) -S localhost -C -U sa -P "$(MSSQL_SA_PASSWORD)" -i ./src/_bootstrap/management/sql/mssql/create_db.sql
endif

reset-migrations:
	rm -f src/dashboard/migrations/0001_initial.py
	rm -f src/_world_api/migrations/0001_initial.py

migrate: validate
	python src/manage.py makemigrations --settings=$(SETTINGS)
	python src/manage.py migrate --settings=$(SETTINGS)

superuser: validate
	python src/manage.py auto_create_superuser --settings=$(SETTINGS)

sample-data: validate
	python src/manage.py sample_data --settings=$(SETTINGS)

reset-sqlite:
	make reset-db SETTINGS=prysent.settings.sqlite3

reset-mssql:
	make reset-db SETTINGS=prysent.settings.mssql

reset-postgres:
	make reset-db SETTINGS=prysent.settings.postgres

reset-db: validate create-db reset-migrations migrate superuser sample-data

media: validate
	python ./src/manage.py upload_media --settings=$(SETTINGS)

media-sqlite:
	make media SETTINGS=prysent.settings.sqlite3

run-sqlite:
	make run SETTINGS=prysent.settings.sqlite3

run-mssql:
	make run SETTINGS=prysent.settings.mssql

run-postgres:
	make run SETTINGS=prysent.settings.postgres

run: validate
	python ./src/manage.py runserver 8875 --settings=$(SETTINGS)

test: validate
	cd src && python manage.py test --settings=$(SETTINGS) && cd ..

voila:
	voila ./media --port=8876 --no-browser --Voila.tornado_settings="{'headers':{'Content-Security-Policy': 'frame-ancestors http://127.0.0.1:8875 http://localhost:8875'}}" &
