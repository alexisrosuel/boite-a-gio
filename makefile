#!/bin/bash

requirements:
				pip3.8 install -r requirements.txt

deploy:
				git add .
				git commit -m 'update'
				git push
				git push heroku main
