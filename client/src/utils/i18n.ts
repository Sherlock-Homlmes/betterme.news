import { ui, defaultLang } from "../i18n/ui";

function getLangFromUrl(url: URL) {
	const [, lang] = url.pathname.split("/");
	if (lang in ui) return lang as keyof typeof ui;
	return defaultLang;
}

function useTranslations(lang: keyof typeof ui) {
	return function t(key: keyof (typeof ui)[typeof defaultLang]) {
		return ui[lang][key] || ui[defaultLang][key];
	};
}

export const translation = (url: URL) => {
	const lang = getLangFromUrl(url);
	return useTranslations(lang);
};
