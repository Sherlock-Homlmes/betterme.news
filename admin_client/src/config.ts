const config = useRuntimeConfig()
const devServerLink = 'http://localhost'
const prodServerLink = 'https://api.betterme.news'
const fetchLink = config.public.isDev ? `${devServerLink}/api` : `${prodServerLink}/api`
export default fetchLink;
