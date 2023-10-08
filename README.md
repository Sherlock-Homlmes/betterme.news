
### PORT: http://localhost
* All bash command in `others/` must be use in project root directory
## REQUIREMENTS:
    - Linux
    - Python >= 3.12
    - Bunjs >= 1.0.4

## SETUP:
    bash others/model_to_ts/setup.sh

## RUN SERVICES:
    - docker compose up -d
    - docker compose logs <service_name> -f --tails=50

## RUN TOOLS:
    - bash others/model2ts.sh
