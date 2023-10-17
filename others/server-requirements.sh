docker compose run --rm server poetry export --without-hashes --without-urls | awk '{ print $1 }' FS=';' > ./server/requirements.txt
