from flet import (
    Column,
    Container,
    Text,
    UserControl,
    padding,
    Image,
    ImageFit,
    ElevatedButton,
    icons,
    AlertDialog,
    TextButton,
    MainAxisAlignment
)
from downloader import song_downloader
from ytmusicapi import YTMusic


class TracksList(UserControl):
    def __init__(self, track_name, artists, album, release_date, album_image, page_):
        super().__init__()
        self.track_name = track_name
        self.artists = artists
        self.album = album
        self.release_date = release_date
        self.album_image = album_image
        self.page_ = page_

    def close_dlg(self, e):
        self.dlg.open = False
        self.page_.update()

    def check_print(self, e):
        self.dlg = AlertDialog(
            title=Text("Download Completed!"), content=Text(f"Finished Downloading {self.track_name}"),
            actions=[
                TextButton("Ok", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        ytmusic = YTMusic()
        results = ytmusic.search(f"{self.track_name} {self.album} {self.artists}", "songs")
        youtube_link = "https://music.youtube.com/watch?v=" + results[0]['videoId']
        song_downloader(youtube_link, {"title": self.track_name, "cover": self.album_image, "artist": self.artists,
                                       "album": self.album})
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def build(self):
        return Container(
            padding=padding.symmetric(horizontal=20, vertical=50),
            content=Column(
                controls=[
                    Image(
                        src=self.album_image,
                        fit=ImageFit.COVER,
                        height=200,
                        # width=64
                    ),
                    Text(self.track_name, size=30),
                    Text(self.artists, size=20),
                    Text(self.album, size=20),
                    Text(self.release_date, size=20),
                    ElevatedButton(text="Download Now", on_click=self.check_print, icon=icons.DOWNLOAD)

                ]
            )
        )
