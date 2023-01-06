import os

import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import EasyMP3


def download_artwork(url):
    """
    This function download the cover for the song and save it in the Downloads folder as temp.jpeg.
    input: url (string) - the url of the cover
    """

    response = requests.get(url)
    return response.content


def song_downloader(url, song_json):
    """
    This function is used to download the song from the youtube link.
    Add's Meta data to song by searching the spotify api and
    Saves it in the Downloads Folder.

    input: url (string) - the url of the song to be downloaded
    input: song_json (dict) - the meta data of the song

    """

    print(f"[*] Downloading {song_json['title']} .........>")

    os.popen(
        f'yt-dlp -x --audio-format mp3 --audio-quality 0 -o "Downloads/{song_json["title"]}.%(ext)s" {url}'
    ).read()
    mp3_file = EasyMP3(f'Downloads/{song_json["title"]}.mp3')
    EasyID3.RegisterTextKey('Cover', 'APIC')
    mp3_file.tags['ARTIST'] = song_json['artist']
    mp3_file.tags['ALBUM'] = song_json['album']
    mp3_file.tags["TITLE"] = song_json["title"]
    mp3_file.save()

    id3 = ID3(f'Downloads/{song_json["title"]}.mp3')
    id3.add(APIC(3, 'image/jpeg', 3, 'Front cover', download_artwork(song_json['cover'])))

    id3.save(v2_version=3)

    print(f"[*] Finished Downloading {song_json['title']}")
