import os
from typing import Any
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler



def images_download(crawler_name: Any, images_count: int) -> None:
    """
    download images
    """
    try:
        crawler_name.crawl(keyword="hedgehog", max_num=images_count)

        print("download finished")

    except Exception as e:

        raise RuntimeError(f"somthing error :(\n {e}") from e

def crawler_initial(crawler_name: str, craw_res: str) -> Any:
    """
    initial crawler
    """

    crawlers_accept = {
        "google": GoogleImageCrawler,
        "bing": BingImageCrawler,
        "flic": FlickrImageCrawler
    }

    if crawler_name not in crawlers_accept:
        raise ValueError(f"bad crawler source: {crawler_name}")

    return crawlers_accept[crawler_name](storage={'root_dir': craw_res})

