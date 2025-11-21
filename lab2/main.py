import argparse
import os
from icrawler.builtin import BingImageCrawler

def parse_args() -> argparse.Namespace:
	"""
    Парсинг параметров с консоли
    """
	parser = argparse.ArgumentParser()
	parser.add_argument("--output", "-o", type=str, required=True, help="Путь к папке для сохранения изображений")
	parser.add_argument("--keywords", "-k",nargs='+', type=str, required=True, help="Ключевое слово для скачивания изображений")
	return parser.parse_args()

def download_images(output_dir=str, keywords=set) -> None:
	for kword in keywords:
		range_dir = os.path.join(output_dir,kword)
		os.makedirs(range_dir, exist_ok=True)
		crawler = BingImageCrawler(storage={'root_dir':range_dir})
		crawler.crawl(keyword=kword)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

def main() -> None:
	""""""
	args = parse_args()
	download_images(args.output, args.keywords)
    
    



if __name__ == "__main__":
	main()