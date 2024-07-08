import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";
import tailwind from "@astrojs/tailwind";
// import partytown from "@astrojs/partytown";
import { loadEnv } from "vite";

const configMap = {
	original: {
		site: "https://betterme.news/",
		publicDir: "./public",
		srcDir: "./src",
		defaultLocale: "vi",
	},
	scholarship: {
		site: "https://scholarship.betterme.news/",
		publicDir: "./public/scholarship-public",
		srcDir: "./scholarship-src",
		defaultLocale: "en",
	},
};
const { ORIGIN } = loadEnv(process.env.NODE_ENV, process.cwd(), "");
const origin = ORIGIN ?? "original";

// https://astro.build/config
export default defineConfig({
	output: "server",
	adapter: cloudflare(),
	site: configMap[origin].site,
	publicDir: configMap[origin].publicDir,
	srcDir: configMap[origin].srcDir,

	trailingSlash: "always",
	markdown: {
		drafts: true,
		shikiConfig: {
			theme: "material-theme-palenight",
			wrap: true,
		},
	},
	integrations: [
		tailwind(),
		// partytown()
	],
	i18n: {
		defaultLocale: configMap[origin].defaultLocale,
		locales: ["en", "vi"],
		routing: {
			prefixDefaultLocale: false,
		},
	},
});
