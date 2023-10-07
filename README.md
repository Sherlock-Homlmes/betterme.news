### SETUP:

    - docker compose build
    - docker compose run --rm server poetry install
    - docker compose run --rm server pre-commmit install
    - docker compose run --rm client npm install

### RUN:

    - docker compose up -d
    - docker compose logs <service_name> -f --tails=50

### CONVERT RESPONSE MODEL TO TYPESCRIPT

    * This command must be use in project root directory
    - Setup: bash others/model_to_ts/setup.sh
    - Run: bash others/model_to_ts/run.sh
