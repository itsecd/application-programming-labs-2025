import argparse
import os

from config import NATURE_SOUNDS_URL
from file_utils import download_sounds
from iterator import AudioFileIterator
from web_scraper import fetch_nature_sounds


def parse_args():
    """Parse command line arguments for the Mixkit nature sounds downloader.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Mixkit nature sounds downloader"
    )
    parser.add_argument(
        "--folder",
        required=True,
        help="Path to folder for saving sounds"
    )
    parser.add_argument(
        "--csv",
        required=True,
        help="Path to CSV annotation file"
    )
    parser.add_argument(
        "--min_files",
        type=int,
        default=50,
        help="Minimum number of files"
    )
    parser.add_argument(
        "--max_files",
        type=int,
        default=100,
        help="Maximum number of files"
    )

    return parser.parse_args()


def main():
    """Main function to orchestrate the nature sounds downloading process."""
    args = parse_args()

    print("Downloading nature sounds from Mixkit.co")
    print(f"Folder: {args.folder}")
    print(f"Annotation: {args.csv}")
    print(f"Target: from {args.min_files} to {args.max_files} files")

    # Check for existing files
    existing_files = []
    if os.path.exists(args.folder):
        existing_files = [
            f for f in os.listdir(args.folder) 
            if f.endswith('.mp3')
        ]
        print(f"Found {len(existing_files)} existing files")

    print("\nSearching for nature sounds...")
    
    # Define categories to search
    categories = [
        "https://mixkit.co/free-sound-effects/nature/",
        "https://mixkit.co/free-sound-effects/forest/", 
        "https://mixkit.co/free-sound-effects/water/",
        "https://mixkit.co/free-sound-effects/weather/",
        "https://mixkit.co/free-sound-effects/birds/"
    ]
    
    # Collect sounds from all categories
    all_sounds = []
    for category_url in categories:
        print(f"\nParsing category: {category_url}")
        remaining_slots = args.max_files - len(all_sounds)
        sounds = fetch_nature_sounds(category_url, remaining_slots)
        all_sounds.extend(sounds)
        
        if len(all_sounds) >= args.max_files:
            all_sounds = all_sounds[:args.max_files]
            break

    if not all_sounds:
        print("No nature sounds found")
        return

    print(f"\nTotal sounds found: {len(all_sounds)}")

    # Download sounds and create annotation
    downloaded_count = download_sounds(all_sounds, args.folder, args.csv)
    
    # Print download results
    print(f"\nDownload results:")
    print(f"Successfully downloaded: {downloaded_count} files")
    print(f"Skipped: {len(all_sounds) - downloaded_count} files")

    if downloaded_count < args.min_files:
        print(f"WARNING: Only {downloaded_count} files downloaded out of minimum required {args.min_files}")
        print(f"Try running the script again to resume downloading")
    else:
        print(f"Success! Downloaded {downloaded_count} files")

    # Demonstrate iterator functionality if files were downloaded
    if downloaded_count > 0:
        print("\n" + "=" * 50)
        print("ITERATOR DEMONSTRATION")
        print("=" * 50)

        print("\nIterator from annotation file:")
        try:
            iterator_csv = AudioFileIterator(args.csv)
            print(f"Total files in iterator: {len(iterator_csv)}")

            print("\nFirst 5 files:")
            for i, path in enumerate(iterator_csv):
                if i < 5:
                    print(f"  {i+1}. {os.path.basename(path)}")
                else:
                    break
        except Exception as e:
            print(f"Error creating iterator from CSV: {e}")

        print("\nIterator from folder:")
        try:
            iterator_folder = AudioFileIterator(args.folder)
            print(f"Total files in iterator: {len(iterator_folder)}")

            print("\nFirst 5 files:")
            for i, path in enumerate(iterator_folder):
                if i < 5:
                    print(f"  {i+1}. {os.path.basename(path)}")
                else:
                    break
        except Exception as e:
            print(f"Error creating iterator from folder: {e}")
    else:
        print("No downloaded files to demonstrate iterator")


if __name__ == "__main__":
    main()