# docker compose run --rm server poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > ./server/requirements.txt
docker compose run --rm server pip freeze > server/requirements.txt
