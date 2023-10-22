# create sample .env file
bash others/create_sample_env.sh
pip install poetry
# install dependencies
cd server
poetry install --only-root
# run test
pytest
