from pytube import YouTube
from moviepy.editor import *
import os

def get_single_song(url, path):
    #initialize YouTube lib
    yt = YouTube(url)
    #get stream
    stream = yt.streams.filter(only_audio=True).first()
    #get title
    song_title = stream.title
    #download
    stream.download(output_path=path, filename=song_title)
    
    conv = AudioFileClip(song_title+'.mp4')
    conv.write_audiofile(song_title+'.mp3')
    conv.close()
    os.remove(song_title+'.mp4')
    

get_single_song('https://www.youtube.com/watch?v=791z7Nb985Y', 'C:\\Users\\Marcin\\Desktop\\Python\\python-youtube-mp3')