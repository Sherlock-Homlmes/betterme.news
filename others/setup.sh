docker compose build
docker compose run --rm server poetry install
docker compose run --rm client npm install

git config --unset-all core.hooksPath

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
cd others
pre-commit install

bun install
