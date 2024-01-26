const isProd = import.meta.env.PROD
const devServerLink = 'http://server:8080'
const prodServerLink = 'https://api.betterme.news'
const fetchLink = isProd ? `${prodServerLink}/api`: `${devServerLink}/api`
export default fetchLink;
