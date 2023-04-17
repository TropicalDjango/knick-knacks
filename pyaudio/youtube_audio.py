#! /usr/bin/env python3

from __future__ import unicode_literals
import yt_dlp as youtube_dl
import readline
import subprocess
from colorama import Fore, Style

def progress_hook(d):
    if d['status'] == 'downloading':
        print("...")
    if d['status'] == 'finished':
        print('\n' + Fore.GREEN + 'Done'.center(20,"_") + Style.RESET_ALL)


ydl_opts = {
    'format': 'bestaudio',
    'continue': True,
    'progress_hooks': [progress_hook],
    'outtmpl': 'downloads/%(title)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def bash_filename(file_name):
    file_name = "\ ".join(file_name.split(" "))
    file_name = "\(".join(file_name.split("("))
    file_name = "\)".join(file_name.split(")"))
    file_name = "\&".join(file_name.split("&"))
    file_name = "\\'".join(file_name.split("'"))
    file_name = '\\"'.join(file_name.split('"'))
    return file_name


def rename_file(old_title, new_title):
    file_name = bash_filename(old_title + ".mp3")
    new_file_name = bash_filename(new_title + ".mp3")
    cmd_string = "mv downloads/{} downloads/{}".format(file_name,
                                                       new_file_name)
    print(cmd_string)
    subprocess.run(cmd_string, shell=True)


def list_downloads():
    cmd_str = "exa -l downloads | awk '{$1=$2=$3=$4=$5=$6=False; print $0}'"
    subprocess.run(cmd_str, shell=True)
    print('\n')
    return


def search(arg):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)
    return video


def search_results(arg):
    ii = 0
    video = search(arg)
    video_url = video['webpage_url']
    video_title = video['title']
    video_thumbnail = video['thumbnail']

    print(Fore.BLUE + str(ii) + " Title: {} \nThumbnail: {} \nURL: {}"
          .format(video_title, video_thumbnail, video_url))

    usr = input(Style.RESET_ALL + "Would you like to download Audio " +
                                    "(y/N/[r]ename): ")
    if usr.lower() == "y" or usr.lower() == "r":
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(video_url)
        if usr.lower() == "r":
            new_title = input("Rename to: ")
            rename_file(video_title, new_title)
    else:
        return


def download_yt_audio(yt_url):
    youtube_dl.YoutubeDL(ydl_opts).extract_info(yt_url)


if __name__ == "__main__":
    print(Fore.GREEN + "Youtube Audio Downloader".center(40, "_"))
    while True:
        print(Style.RESET_ALL + "Select an Option".center(40, "_"))
        print("1: Download from URL \n2: Search for music" +
              "\n3: List of all music \n4: Rename file \n5: Exit")
        arg = input("-> ")
        if arg == '1':
            print("Enter URL".center(40, "_"))
            url = input("-> ")
            download_yt_audio(url)
        elif arg == '2':
            print("Enter Search Term".center(40, "_"))
            term = input("-> ")
            search_results(term)
        elif arg == '3':
            list_downloads()
        elif arg == '4':
            list_downloads()
            video_title = input("old file name: ")
            new_title = input("rename to: ")
            rename_file(video_title, new_title)
        elif arg == '5':
            exit()

