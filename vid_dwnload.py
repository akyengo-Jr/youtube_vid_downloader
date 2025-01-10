import os
import requests
from bs4 import BeautifulSoup
import streamlit as st

def b_filesize(size):
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
    k = 0
    for k in range(len(units)):
        if size < (1024 ** (k + 1)):
            break
    return "%4.2f %s" % (round(size / (1024 ** (k)), 2), units[k])

def download_video(url, output_file, verbose):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    sources = {}

    meta = soup.find('meta', attrs={"property": "og:video"})
    if meta is not None:
        sources["og_video"] = meta['content']

    meta = soup.find('meta', attrs={"property": "og:video:url"})
    if meta is not None:
        sources["og_video_url"] = meta['content']

    meta = soup.find('meta', attrs={"property": "og:video:secure_url"})
    if meta is not None:
        sources["og_video_secure_url"] = meta['content']

    if verbose:
        st.write("Extracted video urls:")
        if "og_video" in sources.keys():
            st.write(f"  - og_video: {sources['og_video']}")
        if "og_video_url" in sources.keys():
            st.write(f"  - og_video_url: {sources['og_video_url']}")
        if "og_video_secure_url" in sources.keys():
            st.write(f"  - og_video_secure_url: {sources['og_video_secure_url']}")

    for source_name in sources.keys():
        video_url = sources[source_name]
        r = requests.head(video_url)
        if r.headers["Content-Type"] in ["video/mp4"]:
            total_size = 0
            if 'Content-Length' in r.headers.keys():
                total_size = str(r.headers['Content-Length'])

            if output_file is not None:
                filename = output_file
            else:
                filename = os.path.basename(video_url).split("?")[0]

            st.write(f"Downloading to {os.path.basename(filename)} ...")
            total_size = 0
            with requests.get(video_url, stream=True) as r:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=16 * 1024):
                        f.write(chunk)
                        total_size += len(chunk)
                        st.progress(total_size / int(r.headers.get('content-length', 1)))
            st.write(f"Downloaded {b_filesize(total_size)} to {os.path.basename(filename)} ...")
            break
        else:
            st.write(f"Unknown Content-Type {r.headers['Content-Type']} for source '{source_name}', skipping")

# Streamlit app
st.title("Streamable Video Downloader")

url = st.text_input("Streamable URL", "")
output_file = st.text_input("Output File (optional)", "")
verbose = st.checkbox("Verbose mode")

if st.button("Download"):
    if url:
        download_video(url, output_file, verbose)
    else:
        st.error("Please provide a Streamable URL")
