import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import cloudflare from '@astrojs/cloudflare'
import sitemap from '@astrojs/sitemap'
import tailwind from '@astrojs/tailwind'

import partytown from '@astrojs/partytown'

// https://astro.build/config
export default defineConfig({
	output: 'server',
	adapter: cloudflare(),
	site: 'https://betterme.news/',
	// Write here your website url
	markdown: {
		drafts: true,
		shikiConfig: {
			theme: 'material-theme-palenight',
			wrap: true,
		},
	},
	integrations: [sitemap(), tailwind(), partytown()],
})
