import streamlit as st
import youtube_dl

def download_video(url):
    ydl_opts = {
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        },
        'extractor_retries': 3,
        'format': 'best',
        'noplaylist': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        st.write(f"Downloading: {title}")
        ydl.download([url])

st.title("YouTube Video Downloader")
url = st.text_input("Enter YouTube video URL")
if st.button("Download"):
    download_video(url)
