/// <reference path="../.astro/types.d.ts" />
interface ImportMetaEnv {
	readonly ENVIRONMENT: string;
	readonly ORIGIN: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
