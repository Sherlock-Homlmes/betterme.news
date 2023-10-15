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
export interface CrawlersData {
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface CrawlersDataParams {
  origin: string;
}
export interface DiscordContent {
  content: (string | string[])[];
}
export interface GetCrawlersDataResponse {
  discord: KhoahocTvDiscordPost | IvolunteerDiscordPost;
  html: KhoahocTvHtmlPost | IvolunteerHtmlPost;
}
export interface KhoahocTvDiscordPost {
  content: (string | string[])[];
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface IvolunteerDiscordPost {
  content: (string | string[])[];
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface KhoahocTvHtmlPost {
  content: string;
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface IvolunteerHtmlPost {
  content: string;
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface HtmlContent {
  content: string;
}
export interface PatchBotPayload {
  start?: boolean;
  stop?: boolean;
}
export interface PatchCrawlersDataPayload {
  origin: string;
  banner?: string;
  thumbnail?: string;
  discord_content: (string | string[])[];
  discord_description: string;
  html_content: string;
  html_description: string;
}
export interface PostCrawlersDataPayload {
  origin: string;
  post_name: string;
  banner?: string;
  thumbnail?: string;
  discord_content: (string | string[])[];
  discord_description: string;
  html_content: string;
  html_description: string;
  is_testing?: boolean;
}
