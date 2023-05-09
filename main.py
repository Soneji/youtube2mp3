from collections import namedtuple
import streamlit as st
import yt_dlp
import zipfile
import glob
import os

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
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info("{}".format(url))
            filename = ydl.prepare_filename(result)
            error_code = ydl.download(url)
    except Exception as e:
        st.error("Error: {}".format(e))
        return

def list_mp3s():
    try:
        files = []
        for file in glob.glob("*.mp3"):
            files.append(file)
        # sort files by name
        files.sort()
        return files
    except Exception as e:
        st.error("Error: {}".format(e))
        return

def cleanup():
    try:
        os.system("rm *.mp3")
        os.system("rm out.zip")
    except Exception as e:
        st.error("Error: {}".format(e))
        return

def generate_zip():
    try:
        os.system("rm out.zip")
        files = list_mp3s()
        with zipfile.ZipFile('out.zip', 'w') as zipMe:
            for file in files:
                print("Adding {} to zip".format(file))
                zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
    except Exception as e:
        st.error("Error: {}".format(e))
        return

url = st.text_input('URL')
st.button("Step 1. Download MP3 files", on_click=lambda: download())
st.button("Step 2. Generate zip", on_click=lambda: generate_zip())

"Download zip button will show once zip is generated successfully"
# if file exists
if os.path.exists("out.zip"):
    with open("out.zip", "rb") as f:
        st.download_button(label='Step 3. Download zip', data=f, file_name='out.zip', mime='application/zip')

"You can clean up the system if you wish to download another playlist or encounter any errors"
st.button("(Optional) Clean up system", on_click=lambda: cleanup())

"Files downloaded:"
st.code('\n'.join(list_mp3s()), language='text')
