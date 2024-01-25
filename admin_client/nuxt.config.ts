// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

export default defineNuxtConfig({
  alias: {
      "@": "./src",
      "@components": "./src/components",
  },
  build: {
    transpile: ['vuetify'],
  },
  devtools: { enabled: true },
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    //...
  ],
  vite: {
    vue: {
      template: {
        transformAssetUrls
      },
    },
  },
  runtimeConfig: {
    public: {
      fetchLink: process.env.DEV
      ? 'http://localhost/api'
      : 'https://api.betterme.news/api'
    }
  }
})
