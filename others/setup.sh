# build docker and install package
docker compose build
docker compose run --rm server poetry install --only-root
docker compose run --rm admin-server poetry install --only-root
docker compose run --rm client npm install --no-save

bash others/create_sample_env.sh

# install common tools
bun install

python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
git config --unset-all core.hooksPath
pre-commit install
