// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
// CommonJS require syntax
const vuePugPlugin = require('vue-pug-plugin')

export default defineNuxtConfig({
  devtools: { enabled: true },
  build: {
    transpile: ['vuetify'],
  },
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
        transformAssetUrls,
        preprocessOptions: { // 'preprocessOptions' is passed through to the pug compiler
          plugins: [
            vuePugPlugin
          ]
        }
      },
    },
  },
})
