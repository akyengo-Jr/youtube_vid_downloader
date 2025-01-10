import streamlit as st
import yt_dlp

def download_video(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        st.write(f"Downloading: {title}")
        ydl.download([url])

st.title("YouTube Video Downloader")
url = st.text_input("Enter YouTube video URL")
if st.button("Download"):
    download_video(url)
