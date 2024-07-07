import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";
import tailwind from "@astrojs/tailwind";

// import partytown from "@astrojs/partytown";

// https://astro.build/config
export default defineConfig({
	output: "server",
	adapter: cloudflare(),
	site: "https://betterme.news/",
	// Write here your website url
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
		defaultLocale: "vi",
		locales: ["en", "vi"],
		routing: {
			prefixDefaultLocale: false,
		},
		domains: {
			en: "https://scholarship.betterme.news",
			vi: "https://betterme.news",
		},
	},
});
