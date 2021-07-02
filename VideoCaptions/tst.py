import speech_recognition as sr 
import moviepy.editor as mp


from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


num_seconds_video= 30*60
print("The video is {} seconds".format(num_seconds_video))
l=list(range(0,num_seconds_video+1,60))
input_video_path = 'video.mp4'
output_video_path = 'converted.mp4'

i = 0;
diz={}
for i in range(0,3):
    
    with VideoFileClip(input_video_path) as video:
      #First 10 seconds
      new = video.subclip(i, i+10)
      new.write_videofile(output_video_path, audio_codec='aac')
      i = i+10

    #ffmpeg_extract_subclip("video.mp4".format(), l[i]-2*(l[i]!=0), l[i+1], targetname="chunks/cut{}.mp4".format())
    clip = mp.VideoFileClip(r"converted.mp4".format(i+1)) 
    clip.audio.write_audiofile(r"converted.wav".format(i+1))
    r = sr.Recognizer()
    audio = sr.AudioFile("converted.wav".format(i+1))
    with audio as source:
      r.adjust_for_ambient_noise(source)  
      audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    #diz['chunk{}'.format(i)]=result

    with open('recognized.txt',mode ='a') as file: 
      file.write(result) 
      file.write("\n") 
      print("Finally ready!")

#l_chunks=[diz['chunk{}'.format(i)] for i in range(len(diz))]
#text='\n'.join(l_chunks)

