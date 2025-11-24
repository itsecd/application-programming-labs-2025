import argparse
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, FlickrImageCrawler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source",
                        help="(google, bing, flickr)")
    parser.add_argument("--storage-dir",
                        help="save folder")
    parser.add_argument("--count", type=int,
                        help="count of images")

    args = parser.parse_args()


    if args.count < 50 or args.count > 1000:
        print("Error: count must be greater than 50 and less than 100.")
        return

    if args.source == 'google':
        crawler = GoogleImageCrawler(storage={'root_dir': args.storage_dir})
    elif args.source == 'bing':
        crawler = BingImageCrawler(storage={'root_dir': args.storage_dir})
    elif args.source == 'flickr':
        crawler = FlickrImageCrawler(storage={'root_dir': args.storage_dir})

    crawler.crawl(keyword='hedgehog', max_num=args.count)
    print(f"Images saved to: {args.storage_dir}")

if __name__ == '__main__':
    main()
