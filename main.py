import yt_dlp
import os
import asyncio
import concurrent.futures
from urllib.parse import urlparse

def get_info(youtube_url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    return info

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
        'writethumbnail': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

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

async def process_url(url, download_type, download_path, max_workers=3):
    video_urls = extract_video_ids(url)
    
    if len(video_urls) == 1:
        if download_type == '1':
            download_video(video_urls[0], download_path)
        else:
            download_audio(video_urls[0], download_path)
        return
    
    download_func = download_video if download_type == '1' else download_audio
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                download_func,
                url,
                download_path
            )
            for url in video_urls
        ]
        
        for completed in await asyncio.gather(*futures):
            print(f"Completed: {completed}")

async def main_async():
    url = input('Enter the YouTube URL: ')
    fileformat = input('Enter the file format: video (1) or audio (2): ')
    max_workers = input('Enter the number of simultaneous downloads (default 2): ')
    
    download_path = 'downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    max_workers = int(max_workers) if max_workers.isdigit() else 2
    
    if fileformat not in ['1', '2']:
        print("Invalid option. Please choose 1 for video or 2 for audio.")
        return
    
    await process_url(url, fileformat, download_path, max_workers)

def main():
    asyncio.run(main_async())

if __name__ == '__main__':
    main()