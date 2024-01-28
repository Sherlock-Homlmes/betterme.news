/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface CrawlerListParams {
  origin: string;
  page?: number;
}
export interface CrawlersDataParams {
  origin: string;
}
export interface GetCrawlersIvolunteerDataResponse {
  id?: string;
  title: string;
  description: string;
  tags: string[];
  banner: string;
  deadline?: string;
  content: string;
  keywords: string[];
}
export interface GetCrawlersKhoahocTvDataResponse {
  title: string;
  description: string;
  tags: string[];
  banner: string;
  thumbnail: string;
  content: string;
  keywords: string[];
}
export interface GetTagsParams {
  origin: string;
}
export interface PatchBotPayload {
  action: string;
}
export interface PatchCrawlersDataPayload {
  title?: string;
  description?: string;
  banner?: string;
  content?: string;
  tags?: string[];
  keywords?: string[];
}
export interface PostCrawlersDataPayload {
  origin: string;
  post_name: string;
}
export interface PostCrawlersPreviewDiscordDataPayload {
  origin: string;
  preview_source: string[];
}
export interface PostCrawlersResponse {
  id: string;
}
/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface GetPostListParams {
  page?: number;
  per_page?: number;
  match_tag?: string;
}
export interface GetPostListResponse {
  id: string;
  slug: string;
  title: string;
  description: string;
  thumbnail_img?: string;
  banner_img?: string;
  tags: string[];
  keywords: string[];
  view: number;
}
export interface GetPostResponse {
  created_at: string;
  title: string;
  description: string;
  thumbnail_img?: string;
  banner_img?: string;
  content: string;
  author: string;
  other_information?: OtherPostInfo;
  view: number;
  tags: string[];
  keywords: string[];
  og_img: string;
}
export interface OtherPostInfo {
  deadline?: string;
}
