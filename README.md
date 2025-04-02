# yt_downloader
This program is a program that can receive links to YouTube videos and download them as mp4 or mp3.

A simple and efficient command-line tool to download YouTube videos as MP4 or extract audio as MP3 using yt-dlp. Features asynchronous operations and multithreading for fast batch downloads.

## Features

- Download YouTube videos in MP4 format
- Extract audio from YouTube videos in MP3 format
- Support for both single videos and playlists
- High-quality audio extraction (320kbps)
- Organized file storage in the 'downloads' directory
- **Multithreaded downloads** for playlists and batch processing
- **Asynchronous operations** for improved performance

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

4. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or equivalent for your distribution

## Usage

Run the program with:
```
python main.py
```

The program will:
1. Prompt you to enter a YouTube URL (video or playlist)
2. Ask whether you want to download as video (1) or audio (2)
3. Ask for the number of simultaneous downloads (default: 3)
4. Download the content to the 'downloads' folder

For playlists, the program will create a subfolder with the playlist name and download multiple videos simultaneously.

## Performance Tips

- For large playlists, adjust the number of simultaneous downloads based on your internet connection
- 3-5 concurrent downloads works well for most home internet connections
- Using too many concurrent downloads might trigger YouTube rate limiting

## Requirements

- Python 3.7+
- yt-dlp
- FFmpeg (for audio extraction and video conversion)

## License
This project is licensed under the [MIT License](LICENSE).