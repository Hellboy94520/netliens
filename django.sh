#!/bin/bash

# PATH
project_path=$PWD
app_path=$project_path/webbook

usage()
{
    echo -e "\e[7mUsage :\e[0m"
    echo -e "\e[1m-a \e[0m: Do all following actions"
    echo -e "\e[1m-b \e[0m: Build application"
    # echo -e "\e[1m-c \e[0m: Collect Static"
    echo -e "\e[1m-l \e[0m: Language"
    echo -e "\e[1m-r \e[0m: Run application"
    echo -e "\e[1m-s \e[0m: Link static and media files"
    echo -e "\e[1m-u \e[0m: Create user"
    exit 0
}

build()
{
    echo -e "---------------------------------------"
    echo -e "\e[7m CLEAR MIGRATIONS \e[0m"
    echo -e "---------------------------------------"
    # Deletion of old migrations files
    migration_path=$app_path/migrations
    find $migration_path -type f -not -name '__init__.py' -delete
    echo -e "Previous migration files deleted \e[92m[OK]\e[0m"
    echo -e "---------------------------------------"
    echo -e "\e[7m BUILD DATABASE \e[0m"
    echo -e "---------------------------------------"
    # Build files to database
    python3 manage.py makemigrations
    [ $? -eq 0 ] && python3 manage.py migrate && \
    echo -e "Migrations files created \e[92m[OK]\e[0m"
    [ $? -ne 0 ] && echo -e "Migrations files created\e[91m [ERROR]\e[0m" && exit 1
}

# collectstatic()
# {
#     # This command will erase /django-project/static with /django-project/app/webbook/static,
#     # So DO NOT USE !
#     echo -e "---------------------------------------"
#     echo -e "\e[7m COLLECT STATIC AND MEDIA \e[0m"
#     echo -e "---------------------------------------"
#     python3 manage.py collectstatic && \
#     echo -e "Collect static and media files \e[92m[OK]\e[0m"
# }

link_static_media()
{
    ln -sf /django_project/static /django_project/app/webbook/
    ln -sf /django_project/media /django_project/app/webbook/
}

language()
{
  echo -e "---------------------------------------"
  echo -e "\e[7m BUILD LANGUAGE \e[0m"
  echo -e "---------------------------------------"
  python3 manage.py makemessages -all && \
  echo -e "Update translation files \e[92m[OK]\e[0m"
  python3 manage.py compilemessages && \
  echo -e "Create translation files \e[92m[OK]\e[0m"
}

user()
{
    echo -e "---------------------------------------"
    echo -e "\e[7m CREATE SUPER USER \e[0m"
    echo -e "---------------------------------------"
    export PYTHONIOENCODING="UTF-8" && \
    python3 manage.py createsuperuser
}

run()
{
    echo -e "---------------------------------------"
    echo -e "\e[7m RUN SERVER \e[0m"
    echo -e "---------------------------------------"
    python3 manage.py runserver 0.0.0.0:8000
}

while getopts 'abclurh' opt
do
  case $opt in
    a) build; language; user; run;;
    b) build;;
    # c) collectstatic;;
    l) language;;
    u) user;;
    r) run;;
    s) link_static_media;;
    h) usage;;
    \*) usage;;
    \?) echo "\e[91mInvalid arguments\e[0m"; usage; exit 1;;
  esac
done
 
exit 0
