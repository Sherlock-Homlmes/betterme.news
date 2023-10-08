### REQUIREMENTS:

    - Linux
    - Python >= 3.12
    - Bunjs >= 1.0.4

### SETUP:

    * This command must be use in project root directory
    bash others/model_to_ts/setup.sh

### RUN:

## Services

    - docker compose up -d
    - docker compose logs <service_name> -f --tails=50

## Convert response model to typescript

    * This command must be use in project root directory
    bash others/model2ts.sh
