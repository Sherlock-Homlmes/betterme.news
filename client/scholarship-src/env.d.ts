/// <reference path="../.astro/types.d.ts" />
interface ImportMetaEnv {
	readonly ORIGIN: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
