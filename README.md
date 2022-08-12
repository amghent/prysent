# prysent

## About

This application is for now a demo application to build an application that will provide an easy way for the data scientists at Arcelor Mittal Ghent to display dashboards built with Jupyter notebooks.

## Technology

### Frontend
- Django 
- Bootstrap

### Backend

- Jupyter notebooks 
- Voila

## Project setup

### conda

Although I'm personally more a fan of poetry (the tool), Arcelor Mittal is using conda for now.  To set up the conda environment for this project, do the following:

````
conda create --name prysent
conda activate prysent

conda install -c conda-forge python
conda install -c conda-forge django
conda install -c conda-forge jinja2
conda install -c conda-forge pyyaml
conda install -c conda-forge pandas
conda install -c conda-forge jupyter
conda install -c conda-forge requests
conda install -c conda-forge voila
conda install -c conda-forge plotly
conda install -c conda-forge psycopg2-binary

pip install mssql-django
````


*Note: the above is for documentation purposes.  Once the environment is created, I will create an export of it. (sidviny)*

### django

A Django project is created under ./src with the following basic commands on the command line:

````
mkdir -p ./src
django-admin startproject prysent ./src/

mkdir -p ./src/dashboard
django-admin startapp dashboard ./src/dashboard
mkdir -p ./src/_world_api
django-admin startapp _world_api ./src/_world_api
````

### Makefile

Yes, make files are typically Linux. But you can also install make on Windows via chocolatey for example.  As I work solely in Linux at home, I prefer to work with make files to do tedious things. (sidviny)

