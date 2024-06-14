# Download Youtube video with Python

This project download Youtube video with Python. 

## Prerequisites

You need to [install Python 3.x](https://wiki.python.org/moin/BeginnersGuide/Download) on your machine. You need also to install `virtualenv`package to create Python Virtual environments.

## How to setup this Project

Here the steps to use this project.

1. Download the source code on your machine:
```
git clone github.com/sasadangelo/download-media
cd download-media
```

2. Create a Python virtual environment and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the requirements:
```
pip3 install -f requirements.txt
```

## How to download a Youtube video

4. Download a Youtube video:
```
python3 -u <youtube URL video> -o <output file>
```

## How to download only the audio of a Youtube video

4. Download only the audio of a Youtube video:
```
python3 -u <youtube URL video> -a -o <output file>
```
