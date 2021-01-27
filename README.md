# nya
Python3 script to download images from the nyafuu archive.

The code is inspired by https://github.com/Exceen/4chan-downloader

## Prerequisites
The script has been tested for Python 3.9

First the required Python packages have to be installed, the suggested way of doing this is using `pip`

On Unix/macOS
```
python3 -m pip install -r requirements.txt
```

On Windows
```
py -m pip install -r requirements.txt
```

## Usage

General
```
python3 nya.py [thread_name]
```

Single image example thread
```
python3 nya.py https://archive.nyafuu.org/bant/thread/12004629/
```

The script checks if an image exists before downloading it, so if your connection gets interrupted or stuck while downloading a thread, you can just run the same command again.