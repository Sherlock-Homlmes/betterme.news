source ./.venv/bin/activate
### server to frontend
pydantic2ts --module ./server/core/schemas/user/responses.py --output ./client/src/types/responses.ts
enumc ./server/core/schemas/user/enums.py --to typescript --out ./client/src/types/enums.ts --sort-enums asc
# replace enum with export enum to import from orther file
sed -i "s/enum/export enum/" ./client/src/types/enums.ts

### server to admin frontend
pydantic2ts --module ./server/core/schemas/user/responses.py --output ./admin_client/src/types/responses.ts
enumc ./server/core/schemas/user/enums.py --to typescript --out ./admin_client/src/types/enums.ts --sort-enums asc
# replace enum with export enum to import from orther file
sed -i "s/enum/export enum/" ./admin_client/src/types/enums.ts
