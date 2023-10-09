# build docker and install package
docker-compose build
docker-compose run --rm server poetry install
docker-compose run --rm admin-server poetry install
docker-compose run --rm client npm install

# create .env file from example.env file
cp server/example.env server/.env
cp admin_server/example.env server/.env

# install common tools
bun install

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
cd others
git config --unset-all core.hooksPath
pre-commit install
