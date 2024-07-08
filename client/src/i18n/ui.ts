export const languages = {
	en: "English",
	vi: "VietNam",
};

const defaultLangMap = {
	original: "vi",
	scholarship: "en",
};
const origin = import.meta.env.ORIGIN ?? "original";
export const defaultLang = defaultLangMap[origin];

export const ui = {
	en: {
		"home.latest_post": "Latest Posts",
		"home.read_post": "Read Post",

		"post.related_posts": "Related posts",
		"post.share": "Share",
		"post.toc": "Table of content",
	},
	vi: {
		"home.latest_post": "Bài viết mới nhất",
		"home.read_post": "Đọc bài",

		"post.related_posts": "Bài viết liên quan",
		"post.share": "Chia sẻ",
		"post.toc": "Nội dung",
	},
} as const;
