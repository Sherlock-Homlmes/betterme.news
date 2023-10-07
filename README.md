### SETUP:

    - docker compose build
    - docker compose run --rm server poetry install
    - docker compose run --rm server pre-commmit install
    - docker compose run --rm client npm install

### RUN:

    - docker compose up -d
    - docker compose logs <service_name> -f --tails=50
