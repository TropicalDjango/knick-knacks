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
    'progress_hooks': [progress_hook],
    'writethumbnail': True,
    'outtmpl': '~/Music/%(title)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }, {
        'key': 'EmbedThumbnail',
    }, {
        'key': 'FFmpegMetadata',
        'add_metadata': True,
    }],
}


def bash_filename(file_name):
    file_name = "\\ ".join(file_name.split(" "))
    file_name = "\\(".join(file_name.split("("))
    file_name = "\\)".join(file_name.split(")"))
    file_name = "\\&".join(file_name.split("&"))
    file_name = "\\'".join(file_name.split("'"))
    file_name = '\\"'.join(file_name.split('"'))
    return file_name


def rename_file(old_title, new_title):
    file_name = bash_filename(old_title + ".mp3")
    new_file_name = bash_filename(new_title + ".mp3")
    cmd_string = "mv ~/Music/{} ~/Music/{}".format(file_name,
                                                       new_file_name)
    print(cmd_string)
    subprocess.run(cmd_string, shell=True)


def list_downloads():
    cmd_str = "exa -1 --icons ~/Music/"
    print('\n')
    subprocess.run(cmd_str, shell=True)
    print('\n')
    return


def search(arg):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries']
        else:
            video = ydl.extract_info(arg, download=False)
    return video


def search_results(arg):
    ii = 0
    video_title = []
    video_url = []
    video_thumbnail = []
    video_list = search(arg)
    for video in video_list:
        video_url.append(video['webpage_url'])
        video_title.append(video['title'])
        video_thumbnail.append(video['thumbnail'])
        print(Fore.BLUE + str(ii) + ": Title: {} \nThumbnail: {} \nURL: {}\n"
              .format(video_title[ii], video_thumbnail[ii], video_url[ii]))
        ii += 1

    usr = input(Style.RESET_ALL + "Would you like to download Audio " +
                                  "([i]/N/[r]ename): ")
    if usr.isdigit() or usr.lower() == "r":
        download_yt_audio(video_url[int(usr)])
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
        match arg:
            case '1':
                print("Enter URL".center(40, "_"))
                url = input("-> ")
                download_yt_audio(url)
            case '2':
                print("Enter Search Term".center(40, "_"))
                term = input("-> ")
                search_results(term)
            case '3':
                list_downloads()
            case '4':
                list_downloads()
                video_title = input("old file name: ")
                new_title = input("rename to: ")
                rename_file(video_title, new_title)
            case '5':
                exit()
