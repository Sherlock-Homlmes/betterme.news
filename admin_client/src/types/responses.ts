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
  title: string;
  description: string;
  banner: string;
  deadline: string;
  content: string;
}
export interface GetCrawlersKhoahocTvDataResponse {
  title: string;
  description: string;
  banner: string;
  thumbnail: string;
  content: string;
}
export interface PatchBotPayload {
  action: string;
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
  title: string;
  banner?: string;
  thumbnail?: string;
  discord_content: (string | string[])[];
  discord_description: string;
  html_content: string;
  html_description: string;
  is_testing?: boolean;
}
