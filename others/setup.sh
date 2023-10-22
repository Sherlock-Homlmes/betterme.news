# build docker and install package
docker compose build
docker compose run --rm server poetry install --only-root
docker compose run --rm admin-server poetry install --only-root
docker compose run --rm client npm install --no-save

# create .env file from example.env file if there are not exist .env file
if [ ! -f ./server/.env ]; then
    echo "Generate server .env file"
    cp server/example.env server/.env
fi
if [ ! -f ./admin_server/.env ]; then
    echo "Generate admin server .env file"
    cp admin_server/example.env admin_server/.env
fi

# install common tools
bun install

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
git config --unset-all core.hooksPath
pre-commit install
