- User port: http://localhost
- User api docs port: http://localhost/api/docs
- Admin port: http://localhost:81
- Database: http://localhost:8081
- All bash command in `others/` must be use in project root directory

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

    - Model to typescript: bash others/model2ts.sh
