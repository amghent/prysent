# prysent

## About

This application allows data scientists at Arcelor Mittal to easily present their notebooks and dashboards without having to worry about a menu structure, Python versions at the client side, ...  All what is needed, is dropping the notebook in a pre-defined location.

## Technology

### Frontend
- Django 
- Bootstrap

### Backend

- Jupyter notebooks 
- nbconvert (Voila has been replaced in version 1.1)

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
conda install -c conda-forge nbconvert
conda install -c conda-forge requests
conda install -c conda-forge plotly
conda install -c conda-forge psycopg2-binary
conda install -c conda-forge croniter

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
````

startapp is done for each sub-directory found in the project.

### Makefile

Yes, make files are typically Linux. But you can also install make on Windows via chocolatey for example.  As I work solely in Linux at home, I prefer to work with make files to do tedious things. (sidviny)

