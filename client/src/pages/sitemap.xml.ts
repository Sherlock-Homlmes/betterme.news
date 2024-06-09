import { siteConfig } from '@/site-config'
import fetchLink from 'src/utils/config'
import type { GetPostListResponse } from '@/types/responses'
import { IvolunteerPageContentTypeEnum } from '@/types/enums'

export async function GET() {
	const siteUrl = import.meta.env.SITE
	const contentTypes = [
		IvolunteerPageContentTypeEnum.VOLUNTEER,
		IvolunteerPageContentTypeEnum.SCHORLARSHIP,
		IvolunteerPageContentTypeEnum.EVENT,
		IvolunteerPageContentTypeEnum.COURSE,
	]
	const getContentTypesSitemapData = async () => {
		return await Promise.all(
			contentTypes.map(async (contentType) => {
				const res = await fetch(`${fetchLink}/posts?per_page=1&match_tags=${contentType}`)
				return await res.json()
			}),
		).then((responses) => {
			return contentTypes.map((contentType, idx) => ({
				contentType,
				lastModified: responses[idx][0].updated_at ?? responses[idx][0].created_at,
			}))
		})
	}
	const contentTypesSitemapData = await getContentTypesSitemapData()

	const result = `
        <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        ${contentTypesSitemapData
					.map((data) => {
						return `<sitemap><loc>${siteUrl}sitemap-${data.contentType}.xml</loc><lastmod>${data.lastModified}+07:00</lastmod></sitemap>`
					})
					.join('\n')}
        </sitemapindex>
    `.trim()

	return new Response(result, {
		headers: {
			'Content-Type': 'application/xml',
		},
	})
}
