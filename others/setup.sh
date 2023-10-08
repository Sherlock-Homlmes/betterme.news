docker compose build
docker compose run --rm server poetry install
docker compose run --rm client npm install

bun install

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
cd others
git config --unset-all core.hooksPath
pre-commit install
