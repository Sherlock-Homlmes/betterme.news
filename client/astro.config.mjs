import { defineConfig } from "astro/config";
import svelte from "@astrojs/svelte";
import cloudflare from "@astrojs/cloudflare";

import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  integrations: [svelte(), tailwind()],
  output: "server",
  adapter: cloudflare(),
});
