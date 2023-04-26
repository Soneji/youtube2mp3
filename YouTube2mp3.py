from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import yt_dlp
import zipfile
import glob, os
import time

"""
# Welcome to YouTube -> MP3 downloader!

Enter the URL of the YouTube video or playlist you wish to download \\
We shall generates a zip of all the MP3s for you :smile:

**Warning: These steps may appear to take a long time, especially for playlists with many long videos** \\
**Please be patient**
"""


def download():
    ydl_opts = {
        'extract_audio': True, 
        'format': 'bestaudio', 
        'outtmpl': '%(title)s.mp3'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info("{}".format(url))
        filename = ydl.prepare_filename(result)
        error_code = ydl.download(url)

def list_mp3s():
    files = []
    for file in glob.glob("*.mp3"):
        files.append(file)
    # sort files by name
    files.sort()
    return files

def cleanup():
    os.system("rm *.mp3")
    os.system("rm out.zip")

def generate_zip():
    files = list_mp3s()
    with zipfile.ZipFile('out.zip', 'w') as zipMe:
        for file in files:
            print("Adding {} to zip".format(file))
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
    
url = st.text_input('URL')
st.button("Download MP3s", on_click=lambda: download())
st.button("Generate zip", on_click=lambda: generate_zip())

"Download zip button will show once zip is generated successfully"
# if file exists
if os.path.exists("out.zip"):
    with open("out.zip", "rb") as f:
        st.download_button(label='Download zip', data=f, file_name='out.zip', mime='application/zip')

st.button("Clean up system", on_click=lambda: cleanup())

"Files downloaded:"
st.code('\n'.join(list_mp3s()), language='text')
