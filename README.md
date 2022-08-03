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
````

*Note: the above is for documentation purposes.  Once the environment is created, I will create an export of it. (sidviny)*

### django

A Django project is created under ./src with the following basic commands on the command line:

````
````

### Makefile

Yes, make files are typically Linux. But you can also install make on Windows via chocolatey for example.  As I work solely in Linux at home, I prefer to work with make files to do tedious things. (sidviny)

