docker-compose run --rm server pip freeze > server/requirements.txt
docker-compose run --rm admin-server pip freeze > admin_server/requirements.txt
