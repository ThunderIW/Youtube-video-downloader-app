import time


import dearpygui.dearpygui as dpg
from pygame import mixer

from main import *


file_path=""
dpg.create_context()
dpg.create_viewport(title='youtuber downloader ', width=700, height=500)



download_option=["Audio","Video"]





def downloadingVideo(sender,data):
    SelectedOption=dpg.get_value("Type")
    default_path="D:\Python Projects\youtube downloader\downloadedVideos(mp4-mp3)"
    output_path=dpg.get_value("path")



    if len(output_path)==0:
        output_path='downloadedVideos(mp4-mp3)'


    video_link = dpg.get_value('videoLink')
    chosen_res=dpg.get_value("-VR-")

    print("res",chosen_res)


    print(output_path,video_link)
    if SelectedOption == "Video":
        download(Audio=False, Video=True, link=video_link,outputPath=output_path,chosen_res=chosen_res)

    if SelectedOption == "Audio":
        download(Audio=True, Video=False, link=video_link,outputPath=output_path,chosen_res="None")

    dpg.set_value("Video_downloaded",True)

    mixer.init()
    mixer.music.load("Google_Pay_Success_Sound_Effect.wav")
    mixer.music.play()





def get_video_info(sender,app_data,user_data):
    youtube_link=dpg.get_value("videoLink")
    title,author,res,filename=get_info(youtube_link)
    print(title)
    print(filename)
    print(res)
    dpg.set_value("VideoTitle",title)
    dpg.set_value("VideoAuthor",author)
    dpg.set_item_width("VideoTitle",width=len(title)+600)
    dpg.set_item_width("VideoAuthor", width=450)
    dpg.configure_item('blank_image',width=720,height=1280)
    width, height, channels, data = dpg.load_image(f"ThumbnailImages/{filename}")
    with dpg.texture_registry():
        dpg.add_static_texture(width=width,height=height,default_value=data,tag=f"{title}+{author}")

    dpg.configure_item("Ythumb",texture_tag=f"{title}+{author}",show=True,height=int(dpg.get_item_height(f"{title}+{author}") * 0.6),width=int(dpg.get_item_width(f"{title}+{author}") * 0.6))
    dpg.set_viewport_height(700)


    dpg.configure_item("T",show=True)
    dpg.set_value("Video_downloaded", False)
    dpg.configure_item("-VR-",items=res)


def play_video(sender,app_data,user_data):

    new_file=file_path.split("\\")
    t=fr"{new_file[0]}\{new_file[1]}\{new_file[2]}\{new_file[3]}"
    play_GIVEN_VIDEO(t,new_file[-1])

def clear(sender,app_data,user_data):
    if user_data=="Clear_Stored_path":
        dpg.set_value("path"," ")
        dpg.set_value("SelectedOutputFile"," ")
    if user_data=="Video_to_played_path":
        dpg.set_value("VideoToPlayedDirectory"," ")



def get_file_path(sender,app_data,user_data):
    print(user_data)
    if user_data=="SettingOut":
        dpg.configure_item("file_dialog_id",show=True)

    if user_data=="GetVideoData":
        video_path=dpg.get_value("path")
        dpg.configure_item("VIDEOFILE",show=True,default_path=video_path)




def ok_pressed(sender,app_data,user_data):

    if user_data=="SettingOutputPath":
        selected_path = app_data["file_path_name"]

        dpg.set_value("path",selected_path)
        dpg.set_value("SelectedOutputFile",str(selected_path).split("\\")[-1])

    if user_data=="SettingVideosArea":
        global file_path

        file_path = list(app_data["selections"].values())[0]
        name_of_file=list(app_data["selections"].keys())[0]
        dpg.set_value("VideoToPlayedDirectory",name_of_file)



def set_view(sender,app_data,user_data):
    download_type=dpg.get_value("Type")

    if download_type=="Video":
        dpg.configure_item("-VR1-",show=True)

    if download_type=="Audio":
        dpg.configure_item("-VR1-",show=False)


def close_app(sender,app_data,user_data):
    dpg.stop_dearpygui()


with dpg.window(label="Window",tag="W1"):

    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Exit",callback=close_app)





    with dpg.tab_bar(label="TB1"):
        with dpg.tab(label="Downloading video or music"):
            dpg.add_text("Please enter the youtube link of the video you would like to download:")
            dpg.add_input_text(hint="Enter link here",tag='videoLink',callback=get_video_info)
            dpg.add_spacing(count=5)

            width, height, channels, data = dpg.load_image("sample_image.png")
            with dpg.texture_registry():
                dpg.add_static_texture(width=width, height=height, default_value=data, tag=f"blank_image")




            dpg.add_text("Image thumbnail",show=False,tag="T")
            dpg.add_image(texture_tag="blank_image",show=False,tag="Ythumb",width=1280,height=720)

            dpg.add_spacing(count=5)

            with dpg.group(horizontal=True,tag="-VR1-",show=False):
                dpg.add_text("Available resolution :")
                dpg.add_radio_button(items=[], tag="-VR-",horizontal=True)  # VR: Video resolution

            dpg.add_spacing(count=5)


            with dpg.group(horizontal=True):
                dpg.add_text("Title:")
                dpg.add_input_text(tag="VideoTitle")
                with dpg.group() as title1:
                    pass
            with dpg.group(horizontal=True,):
                dpg.add_text("Author:")
                dpg.add_input_text(tag="VideoAuthor")
                with dpg.group() as author1:
                    pass

            dpg.add_spacing(count=5)

            dpg.add_text("please select which format would like to download your youtube video")
            dpg.add_radio_button(tag="Type", items=download_option, default_value=download_option[0],callback=set_view)

            dpg.add_checkbox(label="Video downloaded",tag="Video_downloaded")


            dpg.add_button(label="Download", callback=downloadingVideo)


        with dpg.tab(label="Settings"):
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="path",hint="Select the directory you want your video to stored")
                dpg.add_button(label="select output file",callback=get_file_path,user_data="SettingOut")
            with dpg.group(horizontal=True):
                dpg.add_text("output folder:")
                dpg.add_input_text(tag="SelectedOutputFile")
            dpg.add_button(label="Clear", callback=clear,user_data="Clear_Stored_path")



            dpg.add_file_dialog(directory_selector=True, show=False, tag="file_dialog_id", width=500, height=300,callback=ok_pressed,user_data="SettingOutputPath")
        ''''
        with dpg.tab(label="Extra"):
            dpg.add_text("Here you can play your video have fun")


            with dpg.group(label="VideoToPlay",horizontal=True):
                dpg.add_image(texture_tag="blank_image",show=False,tag="ICON_for_playing",width=1280,height=720)
                dpg.add_text("Name of File")
                dpg.add_input_text(hint="Select the video you want to play",tag="VideoToPlayedDirectory")
                dpg.add_button(label="Add",callback=get_file_path,user_data="GetVideoData")


            #dpg.add_file_dialog(directory_selector=False,file_count=5, show=False, tag="VIDEOFILE", width=500, height=300,callback=ok_pressed,user_data="SettingVideosArea",default_filename=".mp4")

            dpg.add_button(label="play",callback=play_video,user_data="h")
            dpg.add_button(label='clear',callback=clear,user_data="Video_to_played_path")
'''



with dpg.file_dialog(directory_selector=False, show=False, callback=ok_pressed, tag="VIDEOFILE", width=700 ,height=400,user_data="SettingVideosArea"):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(38, 45, 239, 255))
    dpg.add_file_extension(".mp4", color=(255, 255, 0, 255))
    dpg.add_file_extension(".mp3", color=(124,252,0))








dpg.setup_dearpygui()
dpg.set_primary_window("W1",True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()