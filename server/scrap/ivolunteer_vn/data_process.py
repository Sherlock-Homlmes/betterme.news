# default
import re
from pathlib import Path
from lxml import etree, html

# library
import aiofiles
import aiohttp
from scrapy import Selector


DATA_DIR = f"{Path(__file__).resolve().parent.parent}/data"


async def save_image(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                img_name = url.split("/")[-1]
                f = await aiofiles.open(f"{DATA_DIR}/media/{img_name}", mode="wb")
                await f.write(await resp.read())
                await f.close()
                return img_name


def replace_html(selector: Selector) -> str:
    content = selector.get()
    replace_tags = (
        ("em", ""),
        ("p", ""),
        ("strong", ""),
    )
    for replace_tag in replace_tags:
        content = content.replace(f"<{replace_tag[0]}>", replace_tag[1]).replace(
            f"</{replace_tag[0]}>", replace_tag[1]
        )
    for replace_tag in replace_tags:
        content = re.sub(f"<{replace_tag[0]}?(.*?)>", replace_tag[1], content, flags=re.DOTALL)

    content = content.replace("<h4>", "").replace("</h4>", "")
    content = content.replace("<li>", "").replace("</li>", "")

    return content


def replace_html_with_discord_tag(selector: Selector) -> str:
    # Check if there are link in selector
    link = None
    if selector.css("a"):
        link = selector.css("a::attr(href)").get()

    # Replace html tag with discord tag
    content = selector.get()
    replace_tags = (
        ("em", "* "),
        ("p", ""),
        ("strong", "** "),
    )
    for replace_tag in replace_tags:
        content = content.replace(f"<{replace_tag[0]}>", replace_tag[1]).replace(
            f"</{replace_tag[0]}>", replace_tag[1]
        )
    for replace_tag in replace_tags:
        content = re.sub(f"<{replace_tag[0]}?(.*?)>", replace_tag[1], content, flags=re.DOTALL)

    content = content.replace("<h4>", "\n**").replace("</h4>", "**")
    content = content.replace("<li>", "\n- ").replace("</li>", "")

    # Replace a tag with link
    if link is not None:
        content = re.sub("<a?(.*?)</a>", "", content, flags=re.DOTALL) + link
    return content


def process_detail_page_data_discord(content: list) -> list:
    new_content = []
    for cont in content:
        if cont.css("ul"):
            temp_cont = cont.css("li")
            cont = [replace_html_with_discord_tag(x) for x in temp_cont]
        else:
            cont = replace_html_with_discord_tag(cont)
        new_content.append(cont)

    # remove empty element
    new_content = [new_cont for new_cont in new_content if new_cont != ""]

    for index, new_cont in enumerate(new_content):
        if isinstance(new_cont, list):
            new_content[index] = [x.replace("  ", " ") for x in new_cont]
        elif isinstance(new_cont, str):
            new_content[index] = new_cont.replace("\xa0", "")
            while "  " in new_content[index] or "** **" in new_content[index]:
                new_content[index] = new_content[index].replace("  ", " ").replace("** **", "**")

    return new_content


def process_detail_page_data_html(content: list) -> list:
    new_content = [cont.get() for cont in content]
    document_root = html.fromstring("".join(new_content))
    return etree.tostring(document_root, encoding="unicode", pretty_print=True)
