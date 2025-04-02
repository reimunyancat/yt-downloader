# YouTube Downloader

A simple and efficient command-line tool to download YouTube videos as MP4 or extract audio as MP3 using yt-dlp.

## Features

- Download YouTube videos in MP4 format
- Extract audio from YouTube videos in MP3 format
- Support for both single videos and playlists
- High-quality audio extraction (320kbps)
- Organized file storage in the 'downloads' directory

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/yt_downloader.git
   cd yt_downloader
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the program with:
```
python main.py
```

The program will:
1. Prompt you to enter a YouTube URL (video or playlist)
2. Ask whether you want to download as video (1) or audio (2)
3. Download the content to the 'downloads' folder

For playlists, the program will create a subfolder with the playlist name.


## Requirements

- Python 3.6+
- yt-dlp
- FFmpeg (for audio extraction and video conversion)

## License
This project is licensed under the [MIT License](LICENSE).
