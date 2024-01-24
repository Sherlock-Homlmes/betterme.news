const isProd = process.env.DEV
const devServerLink = 'http://localhost'
const prodServerLink = 'https://api.betterme.news'
const fetchLink = isProd ? `${prodServerLink}/api`: `${devServerLink}/api`
export default fetchLink;
