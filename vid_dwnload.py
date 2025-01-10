import streamlit as st
from pytube import YouTube
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])

# Docstrings and comments for functions
def get_video_info(url):
    """Fetch video information and available qualities.

    Args:
        url (str): YouTube video URL.

    Returns:
        yt (YouTube): YouTube object.
        available_qualities (list): List of available video qualities.
    """
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
        available_qualities = [stream.resolution for stream in streams]
        return yt, available_qualities
    except Exception as e:
        logging.error(f"Error fetching video info: {e}")
        return None, str(e)


def validate_url(url):
    """Validate the provided YouTube URL.

    Args:
        url (str): YouTube video URL.

    Raises:
        ValueError: If the URL is invalid.
    """
    if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', url):
        raise ValueError("Invalid YouTube URL")


def download_video(url, selected_quality, output_path=None):
    """Download YouTube video based on selected quality.

    Args:
        url (str): YouTube video URL.
        selected_quality (str): Selected video quality.
        output_path (str, optional): Output directory path. Defaults to None.

    Returns:
        success (bool): True if download is successful, False otherwise.
        result (str): Filename if successful, error message otherwise.
    """
    try:
        validate_url(url)

        yt = YouTube(
            url,
            on_progress_callback=on_progress,
            use_oauth=True,
            allow_oauth_cache=True
        )

        # Get appropriate stream
        if selected_quality == 'highest':
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(resolution=selected_quality, progressive=True).first()
            if not stream:
                stream = yt.streams.get_highest_resolution()

        if not stream:
            raise ValueError("No suitable stream found for this video")

        # Create output directory if it doesn't exist
        if output_path:
            os.makedirs(output_path, exist_ok=True)

        # Download video
        filename = stream.default_filename
        stream.download(output_path=output_path)
        logging.info(f"Video downloaded successfully: {filename}")
        return True, filename

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return False, str(e)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_bar.progress(int(percentage))
    status_text.text(f"Downloading... {int(percentage)}%")

# Streamlit UI
st.title('YouTube Video Downloader')

# Create download directory in current working directory
download_dir = os.path.join(os.getcwd(), "downloads")

# URL input
url = st.text_input('Enter YouTube video URL')

if url:
    # Get video information
    yt, available_qualities = get_video_info(url)

    if yt and isinstance(available_qualities, list):
        try:
            st.image(yt.thumbnail_url, use_column_width=True)
            st.write(f"Title: {yt.title}")
            st.write(f"Length: {yt.length // 60}:{yt.length % 60:02d} minutes")
            st.write(f"Views: {yt.views:,}")

            # Quality selection
            qualities = ['highest'] + available_qualities
            selected_quality = st.selectbox('Select video quality', qualities)

            if st.button('Download Video'):
                progress_bar = st.progress(0)
                status_text = st.empty()

                success, result = download_video(url, selected_quality, download_dir)

                if success:
                    progress_bar.progress(100)
                    status_text.text("Download completed!")
                    st.success(f'Video "{result}" has been downloaded to the "downloads" folder!')
                else:
                    st.error(f'Error: {result}')
        except Exception as e:
            logging.error(f"Error processing video: {e}")
            st.error(f"Error processing video: {str(e)}")
    else:
        st.error(f"Unable to fetch video information: {available_qualities}")
