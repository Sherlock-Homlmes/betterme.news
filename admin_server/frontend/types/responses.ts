/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface IvolunteerVnScrapDiscordPostResponse {
  title: string;
  deadline: string;
  banner: string;
  description: string;
  content: (string | string[])[];
}
export interface IvolunteerVnScrapHtmlPostResponse {
  title: string;
  deadline: string;
  banner: string;
  description: string;
  content: string;
}
export interface IvolunteerVnScrapPostResponse {
  title: string;
  deadline: string;
  banner: string;
  description: string;
}
export interface KhoahocTvScrapDiscordPostResponse {}
export interface KhoahocTvScrapHtmlPostResponse {}
export interface KhoahocTvScrapPostResponse {}
export interface ScrapListPostParams {
  origin: string;
  page?: number;
}
export interface ScrapPostParams {
  origin: string;
}
export interface ScrapPostResponse {
  discord: KhoahocTvScrapDiscordPostResponse | IvolunteerVnScrapDiscordPostResponse;
  html: KhoahocTvScrapHtmlPostResponse | IvolunteerVnScrapHtmlPostResponse;
}
