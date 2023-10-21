# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from utils import *

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )



    st.header("Input a YouTube URL to generate subtitles in .md format for Obsidian. ")
    st.write("Ensure that you have the '**Media Extended**' plugin for Obsidian installed beforehand.")
    # Create an input field to enter the URL
    url_yt = st.text_input("Enter a Youtube URL: ")
    st.text("e.g. https://youtu.be/UF8uR6Z6KLc")

# https://www.youtube.com/watch?v=NqVoOC2azZI  # Auto genenerataed subtitles \n
# https://youtu.be/UF8uR6Z6KLc                  # steve job \n
# https://www.youtube.com/watch?v=MpLHMKTolVw   # The NBA Data Scientist \n       ''')

    # Parse and display the URL before the question mark
    if url_yt:
        yt = YouTube(url_yt)
        fn = genFileNamesFromYT(yt)
        file_md = fn["title1"] + '_raw.md'
        f_md = yt2md(yt, file_md)

        st.download_button(
            label = "Download: "+ file_md,
            data = f_md["md"],
            file_name = f_md["fn"]
        )
 

if __name__ == "__main__":
    run()
