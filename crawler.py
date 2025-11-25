from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler, BaiduImageCrawler


def download_images(source, storage_dir, count):
    """Скачивает изображения с использованием icrawler."""
    if source == 'google':
        crawler = GoogleImageCrawler(storage={'root_dir': storage_dir})
    elif source == 'bing':
        crawler = BingImageCrawler(storage={'root_dir': storage_dir})
    elif source == 'flickr':
        crawler = FlickrImageCrawler(storage={'root_dir': storage_dir})
    elif source == 'baidu':
        crawler = BaiduImageCrawler(storage={'root_dir': storage_dir})

    crawler.crawl(keyword='hedgehog', max_num=count, min_size=(200, 200), max_size=(2000,2000))
    print(f"Images saved to: {storage_dir}")