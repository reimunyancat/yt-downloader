import yt_dlp
import os

def get_outtmpl(download_path, info_dict):
    if 'playlist_title' in info_dict and info_dict['playlist_title']:
        return os.path.join(download_path, '%(playlist_title)s/%(title)s.%(ext)s')
    return os.path.join(download_path, '%(title)s.%(ext)s')

def download_video(youtube_url, download_path):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': get_outtmpl(download_path, info),
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

def download_audio(youtube_url, download_path):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': get_outtmpl(download_path, info),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(youtube_url, download=True)

url = input('Enter the YouTube URL: ')
fileformat = input('Enter the file format: video (1) or audio (2): ')
download_path = 'downloads'

if not os.path.exists(download_path):
    os.makedirs(download_path)

if fileformat == '1':
    download_video(url, download_path)
elif fileformat == '2':
    download_audio(url, download_path)
