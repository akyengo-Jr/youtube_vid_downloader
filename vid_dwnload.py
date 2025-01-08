import streamlit as st
from pytube import YouTube

def download_video(url, quality='highest'):
    try:
        yt = YouTube(url)
        if quality == 'highest':
            stream = yt.streams.get_highest_resolution()
        elif quality == 'lowest':
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(res=quality).first()
        stream.download()
        return yt.title
    except Exception as e:
        return str(e)

st.title('YouTube Video Downloader')

url = st.text_input('Enter YouTube video URL')
qualities = ['highest', 'lowest', '360p', '720p', '1080p']
quality = st.selectbox('Select video quality', qualities)

if st.button('Download'):
    if url:
        title = download_video(url, quality)
        st.success(f'Video "{title}" has been downloaded successfully!')
    else:
        st.error('Please enter a valid YouTube URL')
