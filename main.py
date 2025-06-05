import yt_dlp
import os
from urllib.parse import urlparse

def get_info(youtube_url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    return info

def get_cookies_path():
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    return cookies_path if os.path.exists(cookies_path) else None

def download_video(youtube_url, download_path):
    info = get_info(youtube_url)
    
    if 'entries' in info:
        playlist_title = info.get('title', 'playlist')
        playlist_path = os.path.join(download_path, playlist_title)
        if not os.path.exists(playlist_path):
            os.makedirs(playlist_path)
        outtmpl = os.path.join(playlist_path, '%(title)s.%(ext)s')
    else:
        outtmpl = os.path.join(download_path, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': outtmpl,
        'writethumbnail': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'postprocessor_args': [
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '320k'
        ],
        'prefer_ffmpeg': True,
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    cookies_path = get_cookies_path()
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(youtube_url, download=True)
    
    return youtube_url

def download_audio(youtube_url, download_path):
    info = get_info(youtube_url)
    
    if 'entries' in info:
        playlist_title = info.get('title', 'playlist')
        playlist_path = os.path.join(download_path, playlist_title)
        if not os.path.exists(playlist_path):
            os.makedirs(playlist_path)
        outtmpl = os.path.join(playlist_path, '%(title)s.%(ext)s')
    else:
        outtmpl = os.path.join(download_path, '%(title)s.%(ext)s')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'writethumbnail': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    cookies_path = get_cookies_path()
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(youtube_url, download=True)
    
    return youtube_url

def extract_video_ids(url):
    parsed_url = urlparse(url)
    
    if 'youtube.com' in parsed_url.netloc and 'playlist' in parsed_url.path:
        info = get_info(url)
        if 'entries' in info:
            return [entry['id'] for entry in info['entries']]
    elif 'youtube.com' in parsed_url.netloc or 'youtu.be' in parsed_url.netloc:
        return [url]
    
    return [url]

def process_url(url, download_type, download_path):
    video_urls = extract_video_ids(url)
    
    for video_url in video_urls:
        if download_type == '1':
            print(f"Downloading video: {video_url}")
            download_video(video_url, download_path)
        else:
            print(f"Downloading audio: {video_url}")
            download_audio(video_url, download_path)
        print(f"Completed: {video_url}")

def main():
    url = input('Enter the YouTube URL: ')
    fileformat = input('Enter the file format: video (1) or audio (2): ')
    
    download_path = 'downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    if fileformat not in ['1', '2']:
        print("Invalid option. Please choose 1 for video or 2 for audio.")
        return
    
    process_url(url, fileformat, download_path)

if __name__ == '__main__':
    main()