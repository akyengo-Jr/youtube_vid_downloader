import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from pytube import YouTube

def b_filesize(size):
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
    k = 0
    for k in range(len(units)):
        if size < (1024 ** (k + 1)):
            break
    return "%4.2f %s" % (round(size / (1024 ** (k)), 2), units[k])

def download_video(url, output_file, verbose):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    
    if verbose:
        st.write(f"Video Title: {yt.title}")
        st.write(f"Video URL: {video.url}")

    filename = output_file if output_file else yt.title + ".mp4"
    st.write(f"Downloading to {filename} ...")
    video.download(filename=filename)
    st.write(f"Downloaded to {filename}")

def stream_video(url):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').first()
    st.video(video.url)

# Streamlit app
st.title("YouTube Video Downloader and Streamer")

url = st.text_input("YouTube URL", "")
output_file = st.text_input("Output File (optional)", "")
verbose = st.checkbox("Verbose mode")

if st.button("Download"):
    if url:
        download_video(url, output_file, verbose)
    else:
        st.error("Please provide a YouTube URL")

if st.button("Stream"):
    if url:
        stream_video(url)
    else:
        st.error("Please provide a YouTube URL")
