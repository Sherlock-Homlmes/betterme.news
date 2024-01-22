interface SiteConfig {
	author: string
	title: string
	description: string
	lang: string
	ogLocale: string
	shareMessage: string
	paginationSize: number
}

export const siteConfig: SiteConfig = {
	author: 'Little Rookie', // Site author
	title: 'Betterme.news', // Site title.
	description: 'Trang web cung cấp thông tin về  câu lạc bộ, tình nguyện,...', // Description to display in the meta tags
	lang: 'vi',
	ogLocale: 'vi',
	shareMessage: 'Share this post', // Message to share a post on social media
	paginationSize: 6 // Number of posts per page
}
