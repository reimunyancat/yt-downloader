import yt_dlp
import os

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
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(youtube_url, download=True)

def main():
    url = input('Enter the YouTube URL: ')
    fileformat = input('Enter the file format: video (1) or audio (2): ')
    download_path = 'downloads'

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if fileformat == '1':
        download_video(url, download_path)
    elif fileformat == '2':
        download_audio(url, download_path)
    else:
        print("Invalid option. Please choose 1 for video or 2 for audio.")

if __name__ == '__main__':
    main()