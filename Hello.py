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
from helper.utils import *


LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")
    st.write("Generate .md for obsidian from Youtube subtitle")
    # Create an input field to enter the URL
    url_yt = st.text_input("Enter an Youtube URL")

    st.write('''Here are some example urls for you to try:
             https://www.youtube.com/watch?v=NqVoOC2azZI  # Auto genenerataed subtitles
             https://m.youtube.com/watch?v=T3GPIlpKP48     #auto gen subtitle
            https://youtu.be/UF8uR6Z6KLc                  # steve job
            https://youtu.be/eEA0Y54-Ds8                  # think in english
            https://youtu.be/T3GPIlpKP48                  # last date in taiwan
            https://www.youtube.com/watch?v=O6iVsS-RDYI   # Data Commons
            https://www.youtube.com/watch?v=MpLHMKTolVw   # The NBA Data Scientist
            https://www.youtube.com/watch?v=HGHX8OIaupk   # Energy storage breakthroughs
            https://www.youtube.com/watch?v=yeaQUhAOdtk   # How to fight climate change with parking lots
                        
             ''')

    # Parse and display the URL before the question mark
    if url_yt:
        # parsed_url = url_input.split('?')[0]
        # st.write(f"URL before the question mark: {parsed_url}")

        # https://m.youtube.com/watch?v=T3GPIlpKP48     #auto gen subtitle
        # https://youtu.be/UF8uR6Z6KLc                  # steve job
        # https://youtu.be/eEA0Y54-Ds8                  # think in english
        # https://youtu.be/T3GPIlpKP48                  # last date in taiwan
        # https://www.youtube.com/watch?v=O6iVsS-RDYI   # Data Commons
        # https://www.youtube.com/watch?v=MpLHMKTolVw   # The NBA Data Scientist
        # https://www.youtube.com/watch?v=HGHX8OIaupk   # Energy storage breakthroughs
        # https://www.youtube.com/watch?v=yeaQUhAOdtk   # How to fight climate change with parking lots

        yt = YouTube(url_yt)
        # path_md = r'C:\Users\iMonet\OneDrive\文件\obsidian\EnglishTube\000_Inbox' 
        fn = genFileNamesFromYT(yt)
        st.write(fn)
        file_md = fn["title1"] + '_raw.md'
        f_md = yt2md(yt, file_md)

        # import streamlit as st

        # text_contents = '''This is some text'''
        # st.download_button('Download some text', text_contents)        

        st.download_button(
            label = "Download .md file",
            data = f_md["md"],
            file_name = f_md["fn"],
            # mime='text/csv',
        )

        # Create a button to trigger the download
        # if st.button("Download .md file"):
            # st.markdown("[Download .md file](data:text/plain;base64," + st.encode(f_md) + ")")
            # with open(f_md, "w", encoding="utf-8") as file:
            #     file.write(article_content)
            # st.markdown("[Download Article](data:text/plain;base64," + st.encode(article_content).decode() + ")")
            # st.write(f_md)

 

if __name__ == "__main__":
    run()
