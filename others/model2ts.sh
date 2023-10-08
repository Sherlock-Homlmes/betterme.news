source ./.venv/bin/activate
pydantic2ts --module ./server/core/schemas/response.py --output ./client/src/types/response.ts
enumc ./server/core/schemas/enums.py --to typescript --out ./client/src/types/enums.ts --sort-enums asc
sed -i "s/enum/export enum/" ./client/src/types/enums.ts
