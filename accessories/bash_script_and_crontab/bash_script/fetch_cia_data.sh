#!/bin/bash

cd ~
# cd /var/log/sesame/
cd /var/www/prod/scraping_project/media/log/crontab/
current_date=$(date +"%Y-%m-%d_%H-%M-%S")
# current_date=$(date +"%Y-%m-%d")
touch "$current_date-fetch_cia_data.log"
chmod 744 "$current_date-fetch_cia_data.log"

cd ~
cd /var/www/prod/scraping_project/

/var/www/Project_Environments/python_environments/sebpo_scrap_env_312/bin/python3.11 manage.py fetch_cia_data >> /var/www/prod/scraping_project/media/log/crontab/"$current_date-fetch_cia_data.log" 2>&1
