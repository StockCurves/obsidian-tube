

from pytube import YouTube
# from bs4 import BeautifulSoup 
import datetime, srt
import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as ytta
from youtube_transcript_api.formatters import SRTFormatter

# ## Utilities
# - xml2srt(text)
# - getSubs(file_srt)
# 
# - getSRTstatics(file_srt)
# - rmEmoji(text)
# 
# - genFileNamesFromYT(yt)
# - getYAML(yt, file_srt)
# 
# - srt2oneline(file_in, file_out)
# - srt2mergelines(file_in, file_out)
# 
# - yt2srt(yt, file_srt)
# - yt2mp3(yt, file_mp3)
# - yt2md(yt, file_md)
 

def yt2srt(yt, file_srt):    
    transcript_en = ytta.list_transcripts(yt.video_id).find_transcript(['en']).fetch()
    srt_formatted = SRTFormatter().format_transcript(transcript_en)
    with open(file_srt, 'w', encoding='utf-8') as fn:
        fn.write(srt_formatted)    

def getSubs(srt_in):
    with open(srt_in) as f:
        subs = list( srt.parse( f.read()) )
    return subs        

def getSRTstatics(file_srt):
    subs = getSubs(file_srt)
    Ts = 0
    Counts = 0
    for i, sub in enumerate(subs):      
        t1 = int(sub.start.total_seconds() )
        t2 = int(sub.end.total_seconds() ) 
        Ts += t2-t1

    return {
        "total_sec": Ts,
        "total_time": datetime.timedelta(seconds=Ts),
        "num_subs": len(subs)
    }

def getYAMLfromSRT(file_srt):
    info = getSRTstatics(file_srt)
    YAML = """---
file_srt: {}
audio_length: {}
subtitles_length: {}
---
"""
    return YAML.format(file_srt, info['total_time'], info['num_subs'])

def getYAML(yt, file_srt):
    s =  getSRTstatics(file_srt)
    
    title = yt.title
    captions = yt.captions
        
    code = 'a.en'
    codes = [x.code for x in captions.keys()]
    for c in codes:
        if c.startswith('en'):
            code = c
        
    languages = [k.code for k in list(captions.keys())]
    
    YAML = """---
yt_title: {}
yt_author: {}
yt_channel_url: {}
yt_video_url: https://youtu.be/{}
yt_publish_date: {}
yt_rating: {}
yt_views: {}
available_subtitles: {}
video_length: {}
audio_length: {}
subtitles_length: {}
alias: []
date: {}
---
    """
    publish_date = yt.publish_date
    return YAML.format(rmEmoji(yt.title),  
                       rmEmoji(yt.author), 
                       yt.channel_url, 
                       yt.video_id, 
                       yt.publish_date.date(),
                       yt.rating, 
                       yt.views, 
                       languages, 
                       datetime.timedelta(seconds=yt.length), 
                       s["total_time"],
                       s["num_subs"],
                       datetime.date.today())     

def srt2oneline(file_in, file_out):   
    subs = getSubs(file_in);
    for s in subs:              
        subtitle = s.content.replace('\n', ' ').replace('>>', '').replace('&#39;', '\'').strip()
        subtitle = re.sub("[\(\[].*?[\)\]]", "", subtitle)
        if subtitle.startswith('-'):
            subtitle = subtitle[1:].strip()
        s.content = subtitle

    with open(file_out,'w') as f:
        f.write(srt.compose(subs))  

def srt2mergelines(file_in, file_out):
    subs2 = getSubs(file_in);
    sStart = 0
    sEnd = 0
    sDone = 1
    longSentence = []
    
    for i, s in enumerate(subs2):
        subtitle = s.content
        if subtitle[0].isupper() and sDone==1:
            sStart = i
            sDone = 0

        if subtitle[-1]=='.' or subtitle[-1]=='?':
            sEnd = i
            sDone = 1  

        if (sEnd - sStart > 0) and sDone==1:
            pair = [sStart, sEnd]
            longSentence.append(pair)
            subs2[sStart].end = subs2[sEnd].end
            for j in range(sStart+1, sEnd+1):
                subs2[sStart].content += ' ' + subs2[j].content 
                subs2[j].content=''

    with open(file_out,'w') as f:
        f.write(srt.compose(subs2))  

def rmEmoji(text):
    _t = re.sub('[^a-zA-Z0-9|# \' \n\.]', ' ', text).strip()
    _t = [x for x in _t.split(' ')]
    _t2 = []    

    for i, x in enumerate(_t):
        if x !='':
            _t2.append(x)  

    return ' '.join(_t2)

def genFileNamesFromYT(yt):        
    title_original = rmEmoji(yt.title)
    title0 = title_original.split('|')[0]
    title0 = title0.split('#')[0].strip()    
    title1 = title0.replace(" ", "_")
    
    blk = [x[0] for x in title0.split(' ')]
    blk = ''.join(blk[:3])
    fn  = {   
            "title_original": yt.title ,
            "title0": title0,
            "title1": title1, 
            'block': blk   # can only have letters and numbers
        }
    return fn
 
def yt2md(yt, md_out):
    src_media = 'https://youtu.be/' + yt.video_id
    iframe = """
<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
"""
    iframe = iframe.format(yt.video_id) +'\n\n'

    fn = genFileNamesFromYT(yt)
    
    srt_noext = './workspace/' + fn["title1"]
    file_srt0 = srt_noext + '_0.srt'
    file_srt1 = srt_noext + '_1.srt'
    file_srt2 = srt_noext + '_2.srt'
    
    yt2srt(yt, file_srt2)
    srt2oneline(file_srt2, file_srt2)
    srt2mergelines(file_srt2, file_srt2)    
    YAML = getYAML(yt, file_srt2)
    
    subs = getSubs(file_srt2)
    file_md = srt_noext + '_raw.md'
    blockID = '^' + fn["block"].replace('_','')

    # index, subtitle, file_mp3, t1, t2
    row3c = '#### [{}]({}#t={},{})  \n{}  {}{}\n'   #DO NOT Add Space In The Template
    lines = ''
    # thumbnail = '\n![[{}]]\n'.format(yt.thumbnail_url)
    for i, sub in enumerate(subs):      
        t1 = int(sub.start.total_seconds() * 1000)
        t2 = int(sub.end.total_seconds() * 1000)  
        t1_str = sub.start
        t2_str = sub.end
        itemNum = f'{sub.index:04d}'
        subtitle = sub.content   #.replace('\n',' ')    # for captions display?
        lines += '\n' + row3c.format(itemNum,  src_media, t1/1000, t2/1000,  subtitle, blockID, itemNum)  

    title_md = "\n## " + fn["title0"] +'\n'    
    lines = YAML +  title_md + iframe +   lines    

    # st.write(lines)
    with open(md_out, 'w') as f:
        f.write(lines)    

    return {
        "fn": file_md.split('/')[2],            
        "md": lines        
    }
 

