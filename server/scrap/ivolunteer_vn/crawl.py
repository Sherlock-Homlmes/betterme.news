# default
import asyncio
import json
import io
from pathlib import Path

# library
import scrapy
from scrapy.crawler import CrawlerProcess

# local
from data_process import (
    save_image,
    # process_detail_page_data_discord,
    process_detail_page_data_html,
    replace_html,
)

DATA_DIR = f"{Path(__file__).resolve().parent.parent}/data"
ALLOWED_DOMAINS = ["ivolunteer.vn"]
PAGE_URL = "https://ivolunteer.vn/"


# page content
def ivolunteer_crawl(url: str):
    class IvolunteerTvSpider(scrapy.Spider):
        name = "ivolunteer post"
        allowed_domains = ALLOWED_DOMAINS
        start_urls = [PAGE_URL + url]

        def parse(self, response):
            # crawl
            title = response.css("h1::text").get().replace("  ", "").replace("\n", "")
            deadline = response.css(".mvp-post-cat::text").get().replace("Deadline: ", "")
            deadline = "-".join(deadline.split("/")[::-1])
            if deadline in ["ASAP", "All year round"]:
                deadline = None
            banner = response.css("#mvp-content-main").css("img::attr(data-src)").get()
            banner = None if banner is None else asyncio.run(save_image(banner)).split("/")[-1]
            content = response.css("#mvp-content-main").css("h4, p, ul")
            content.pop(0)
            content.pop()
            content.pop()

            general_data = {
                "title": title,
                "description": replace_html(response.css("#mvp-content-main").css("p")[0]),
                "deadline": deadline,
                "banner": banner,
                "content": process_detail_page_data_html(content),
                "tags": [],
                # SEO
                "keywords": [],
            }
            # html_content = process_detail_page_data_html(content)
            # discord_content = process_detail_page_data_discord(content)

            # write to file
            file_name = self.start_urls[0].split("/")[3]

            # write to js file
            with io.open(
                f"{DATA_DIR}/general/{file_name}.json", "w", encoding="utf8"
            ) as html_json_file:
                json.dump(general_data, html_json_file, ensure_ascii=False, indent=4)

    process = CrawlerProcess({"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"})
    process.crawl(IvolunteerTvSpider)
    process.start()


# page with many content
def ivolunteer_page_crawl(content_type: str, page_number: int):
    class IvolunteerPageSpider(scrapy.Spider):
        name = "ivolunteer"
        allowed_domains = ALLOWED_DOMAINS
        start_urls = [f"{PAGE_URL}/{content_type}/page/{page_number}"]

        def parse(self, response):
            data = response.css(".mvp-feat1-mid-wrap").css("a::attr(href)").getall()
            data.extend(response.css(".mvp-feat1-left-wrap").css("a::attr(href)").getall())
            temp_data = response.css(".mvp-feat1-right-wrap").css("a::attr(href)").getall()
            temp_data.pop()
            data.extend(temp_data)
            data.extend(response.css(".mvp-widget-feat1-cont").css("a::attr(href)").getall())
            data.extend(response.css(".mvp-main-blog-cont").css("a::attr(href)").getall())

            # write to js file
            with io.open(
                f"{DATA_DIR}/pages/{content_type}-{page_number}.json",
                "w",
                encoding="utf8",
            ) as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

    process = CrawlerProcess({"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"})
    process.crawl(IvolunteerPageSpider)
    process.start()
