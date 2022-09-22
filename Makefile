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

clean:
	rm -rf ./html_cache

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

ifeq ("$(SETTINGS)", "prysent.settings.prod")
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
	make reset SETTINGS=prysent.settings.sqlite3

reset-mssql:
	make reset SETTINGS=prysent.settings.mssql

reset-postgres:
	make reset SETTINGS=prysent.settings.postgres

reset-prod:
	make reset SETTINGS=prysent.settings.prod

reset: validate create-db reset-migrations migrate superuser


media-sqlite:
	make media SETTINGS=prysent.settings.sqlite3

media-mssql:
	make media SETTINGS=prysent.settings.mssql

media-postgres:
	make media SETTINGS=prysent.settings.postgres

media-prod:
	make media SETTINGS=prysent.settings.prod

media: validate
	python ./src/manage.py upload_media --settings=$(SETTINGS)


clean-cache-sqlite:
	make clean-cache SETTINGS=prysent.settings.sqlite3

clean-cache-mssql:
	make clean-cache SETTINGS=prysent.settings.mssql

clean-cache-postgres:
	make clean-cache SETTINGS=prysent.settings.postgres

clean-cache-prod:
	make clean-cache SETTINGS=prysent.settings.prod

clean-cache: validate
	python ./src/manage.py clean_cache --settings=$(SETTINGS)


schedule-sqlite:
	make schedule SETTINGS=prysent.settings.sqlite3

schedule-mssql:
	make schedule SETTINGS=prysent.settings.mssql

schedule-postgres:
	make schedule SETTINGS=prysent.settings.postgres

schedule-prod:
	make schedule SETTINGS=prysent.settings.prod

schedule: validate
	python ./src/manage.py upload_schedule --settings=$(SETTINGS)


run-sqlite:
	make run SETTINGS=prysent.settings.sqlite3

run-mssql:
	make run SETTINGS=prysent.settings.mssql

run-postgres:
	make run SETTINGS=prysent.settings.postgres

run-prod:
	make run SETTINGS=prysent.settings.prod

run: validate
	python ./src/manage.py runserver 8875 --settings=$(SETTINGS)


run-scheduler-sqlite:
	make run-scheduler SETTINGS=prysent.settings.sqlite3

run-scheduler-mssql:
	make run-scheduler SETTINGS=prysent.settings.mssql

run-scheduler-postgres:
	make run-scheduler SETTINGS=prysent.settings.postgres

run-scheduler-prod:
	make run-scheduler SETTINGS=prysent.settings.prod

run-scheduler: validate
	python ./src/manage.py scheduler --settings=$(SETTINGS)


run-schedule-sqlite:
	make run-schedule SETTINGS=prysent.settings.sqlite3

run-schedule-mssql:
	make run-schedule SETTINGS=prysent.settings.mssql

run-schedule-postgres:
	make run-schedule SETTINGS=prysent.settings.postgres

run-schedule-prod:
	make run-schedule SETTINGS=prysent.settings.prod

run-schedule: validate
	python ./src/manage.py run_schedure --settings=$(SETTINGS)


test: validate
	cd src && python manage.py test --settings=$(SETTINGS) && cd ..

