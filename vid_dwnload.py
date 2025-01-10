import streamlit as st
import yt_dlp

def download_video(url):
    ydl_opts = {
        'proxy': 'http://38.45.44.106:999',  # Replace with your proxy server details
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        st.write(f"Downloading: {title}")
        ydl.download([url])

st.title("YouTube Video Downloader")
url = st.text_input("Enter YouTube video URL")
if st.button("Download"):
    download_video(url)
