### /usr/bin/env bash
#!/bin/bash
# slash_var="/"
# cd DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# base_dir = pwd
# pwd
# ls
# echo "######################################"

find . -path "*/migrations/*.py"  -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete   






### ----------------------------------------------------------------###
# #-- for mysql database --#
# mysql --defaults-extra-file=./my.cnf -e "DROP DATABASE bhutan_adss_db"
# mysql --defaults-extra-file=./my.cnf -e "CREATE DATABASE bhutan_adss_db"

### ----------------------------------------------------------------###






# #-- apply migrations --#
python manage.py makemigrations
python manage.py migrate

# create superuser
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin_rimes', 'admin@myproject.com', 'admin_rimes!@#$')" | python3 `pwd`/manage.py shell









#############################################################################################
### LOAD FIXTURE DATA
############################################################################################# 
# #
# python manage.py loaddata fixture_data/user_authentication/2_geo_level.json

# #
# python manage.py loaddata fixture_data/app_crops/1_crop_type.json



