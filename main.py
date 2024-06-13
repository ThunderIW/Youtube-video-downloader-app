import re
import shutil
import time
import os
from pytube import YouTube
import subprocess
from PIL import Image
import urllib.request

from moviepy.editor import VideoFileClip,AudioFileClip


def get_info(link: str):
    resolution_list = {}
    empty_values = []
    filename = ""
    from datetime import timedelta
    my_video = YouTube(link)
    title = my_video.title
    author = my_video.author
    video_thumbnail = my_video.thumbnail_url

    try:
        if ".png" in video_thumbnail:
            print("PNG")
            url = urllib.request.urlretrieve(video_thumbnail,
                                             f"ThumbnailImages\Thumb.png")
            filename = "Thumb.png"

        if ".jpg" in video_thumbnail:
            print("JPG")
            url = urllib.request.urlretrieve(video_thumbnail,
                                             f"ThumbnailImages\Thumb.jpg")
            filename = "Thumb.jpg"


    except FileNotFoundError:
        pass


    video = my_video.streams.filter(file_extension='mp4')
    for stream in video:
        if not stream.is_progressive:
            resolution_list[stream.itag] = stream.resolution
    for key, value in resolution_list.items():
        if value == None:
            empty_values.append(key)

    for itag in empty_values:
        del resolution_list[itag]

    return title, author, list(resolution_list.values()), filename


def get_thumbnail(link: str):
    my_video = YouTube(link)


def download(Audio: bool, Video: bool, link: str, outputPath, chosen_res: str, download_state=False):
    resolution_list = {}
    empty_values = []
    print("HIT")
    print(link)
    print(outputPath)

    my_video = YouTube(link)

    if Audio == True:
        print("HIT_audio")

        updated_file = re.sub(r'[<>:"/\\|?*]', '', my_video.title)


        my_video.streams.get_audio_only().download(output_path=outputPath, filename=f"{updated_file}.mp3")


    if Video == True:
        for stream in my_video.streams.filter(file_extension='mp4'):
            if stream.is_progressive == False:
                resolution_list[stream.itag] = stream.resolution
        for key, value in resolution_list.items():
            if value == None:
                empty_values.append(key)

        for tag_to_delete in empty_values:
            del resolution_list[tag_to_delete]
        print(resolution_list)
        if len(chosen_res)==0:
            print("HIT")
            chosen_res=list(resolution_list.values())[0]
        tag = next((k for k, v in resolution_list.items() if v == chosen_res), None)
        print(tag)
        chosen_video_to_download = my_video.streams.get_by_itag(tag)
        chosen_video_to_download.download(output_path="download_files", filename="Video_file.mp4")
        my_video.streams.get_audio_only().download(output_path='download_files', filename="Audio_file.mp3")
        '''
        input_audio = "download_files\Audio_file.mp3"
        input_video = "download_files\Video_file.mp4"
        output_file = f"combine_video.mp4"
        ffmpeg_command = [
            'ffmpeg',
            '-i', input_video,  # Input video file
            '-i', input_audio,  # Input audio file
            '-c:v', 'copy',  # Copy the video codec
            '-c:a', 'aac',  # Use the AAC audio codec
            '-strict', 'experimental',  # Allow experimental codecs
            output_file  # Output combined file
        ]
        try:
            result = subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Video and audio combined successfully")
            print("stdout:", result.stdout.decode())
            print("stderr:", result.stderr.decode())
        except subprocess.CalledProcessError as e:
            print("Error during combining video and audio")
            print("stdout:", e.stdout.decode())
            print("stderr:", e.stderr.decode())

        '''
        updated_file = re.sub(r'[<>:"/\\|?*]', '', my_video.title)
        video=VideoFileClip("download_files\Video_file.mp4")
        audio=AudioFileClip("download_files\Audio_file.mp3")
        video_with_audio=video.set_audio(audio)
        video_with_audio.write_videofile("combine_video.mp4", codec="libx264", audio_codec="aac")

        os.rename('combine_video.mp4', f"{updated_file}.mp4")
        try:
            shutil.move(f"{updated_file}.mp4",outputPath)
            os.remove("download_files\Audio_file.mp3")
            os.remove("download_files\Video_file.mp4")
        except Exception as err:
            pass








def Play_video(filename):
    subprocess.call(f"vlc {filename}")


def play_GIVEN_VIDEO(filenamePath, itemToPlay):
    new_fileName = ""

    try:
        os.chdir(f"{filenamePath}")
        subprocess.run(f'vlc "{itemToPlay}" ', shell=True)
    except NotADirectoryError:
        subprocess.run(f'vlc "{itemToPlay}" ', shell=True)

    # if "_" not in filenamePath:
    #    t=filenamePath.split("\\")[-1]
    #    new_fileName=t.replace(" ", "_")
    #    subprocess.call(f'ren "{filenamePath}" {new_fileName}',shell=True)


def convertMp3ToWav(in_file):
    name_of_file = in_file
    name_of_music = name_of_file
    subprocess.call(['ffmpeg', '-i', f'{name_of_music}.mp3',
                     f'{name_of_music}.wav'])
