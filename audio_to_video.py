from moviepy.editor import VideoFileClip, AudioFileClip
import os, random



race = 'MUGELLO'
season = '2024'
all_music_files = os.listdir('/home/boris/Documents/matplotlib_exercize/music')
vf = f'/home/boris/Documents/matplotlib_exercize/{race}_{season}_F1/LapChart.mp4'

mf = '/home/boris/Documents/matplotlib_exercize/music/'+random.choice(all_music_files)
print(mf)
vc = VideoFileClip(vf)
mc = AudioFileClip(mf)
fc = vc.set_audio(mc.subclip(0, vc.duration))
fc.write_videofile('/home/boris/Documents/matplotlib_exercize/MUGELLO_2024/LapChart_with_audio.mp4',  codec="libx264", audio_codec="aac")