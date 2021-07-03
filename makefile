#!/bin/bash

requirements:
				pip3.8 install -r requirements.txt

deploy:
				git add .
				git commit -m 'update'
				git push
				git push heroku main


init_db:
				python3 source/manage.py db init

migrate_db:
				python3 source/manage.py db migrate

upgrade_db:
				python3 source/manage.py db upgrade
