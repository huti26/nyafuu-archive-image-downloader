from bs4 import BeautifulSoup
import requests
import os
import logging
import argparse
from tqdm.auto import tqdm
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = ua.random

log = logging.getLogger('Logger for nyafuu downloader')
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
workpath = os.path.dirname(os.path.realpath(__file__))


def main():
    # description is printed on --help
    parser = argparse.ArgumentParser(
        description='nya is a command-line tool to download threads from the nyafuu archive')
    parser.add_argument(
        'thread',
        nargs=1,
        help='url of the thread, example: https://archive.nyafuu.org/news/thread/775982/'
    )

    # argparse creates a "namespace"
    # using vars() we get a simple dict like
    # {'thread': ['https://archive.nyafuu.org/news/thread/775982/']}
    args = vars(parser.parse_args())

    # read thread & get important info
    url = args.get("thread")[0].strip()
    url_split = url.split("/")
    board_name = url_split[3]
    thread_number = url_split[5]

    # needed against 403
    headers = {
        'User-Agent': user_agent
    }

    # get all image links
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(class_="thread_image_link")

    for link in results:
        image_link = link.get("href")
        image_name = image_link.split("/")[-1]
        file_path = os.path.join(workpath, "downloads", board_name, thread_number, image_name)

        # create the folder structure & file
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # get the header to compare file size
        # if a user aborts downloading a thread, he can continue from where he left off
        response = requests.head(image_link, headers=headers)
        file_download_size = int(response.headers.get('content-length', 0))

        if not os.path.exists(file_path) or os.path.getsize(file_path) < file_download_size:
            # download the image
            log.info(image_link)
            response = requests.get(image_link, headers=headers, stream=True)

            # show a progressbar while downloading
            # save the image to a file
            # file_download_size = int(response.headers.get('content-length', 0))
            with tqdm.wrapattr(open(file_path, "wb"), "write",
                               miniters=1,
                               total=file_download_size) as fout:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)
        else:
            log.info("Skipping %s, image already downloaded.", image_link)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
