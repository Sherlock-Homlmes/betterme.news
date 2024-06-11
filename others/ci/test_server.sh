cd server
python -m pytest --disable-warnings --cov-report term --cov=routers --cov=services --cov=scrap tests/
