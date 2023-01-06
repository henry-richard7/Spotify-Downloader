from flet import (
    app,
    Column,
    Row,
    Page,
    TextField,
    ElevatedButton,
    Image,
    Text,
    ScrollMode,
    Tabs,
    Tab,
    Container
)
from numerize import numerize
from search_songs import search_songs
from spotify import get_playlist, get_album, get_artist_top_10_tracks
from tracks_list import TracksList


def main(page: Page):
    playlist_id = TextField(label="Spotify Playlist ID")
    album_id = TextField(label="Spotify Album ID")
    artist_id = TextField(label="Spotify Artist ID")

    song_search_name = TextField(label="Song To Search")

    page.title = "Spotify Downloader"

    def add_playlist(e):
        if not playlist_id.value:
            playlist_id.error_text = "Playlist ID cannot be empty!"
            page.update()
        else:
            playlist_id_value = playlist_id.value
            playlist_results = get_playlist(playlist_id_value)
            playlist_tracks = []
            for rr in playlist_results['tracks']:
                playlist_tracks.append(TracksList(rr['name'], rr['artist'], rr['album'],
                                                  rr['release_date'], rr['album_image'], page))
            t.tabs[0].clean()
            t.tabs[0].content = Column(
                controls=[
                    Container(
                        margin=10,
                        content=playlist_id
                    ),
                    ElevatedButton("Get Playlist!", on_click=add_playlist),
                    Row(controls=[
                        Image(src=playlist_results['cover'], height=260),
                        Column(controls=[
                            Text(playlist_results['title'], size=40),
                            Text(playlist_results['description'], size=25),
                            Text(f"Followers: {numerize.numerize(playlist_results['followers'])}", size=25),
                        ])
                    ]),
                    Column(controls=playlist_tracks)

                ], scroll=ScrollMode.ALWAYS
            )
            t.tabs[0].update()

    def add_albums(e):
        if not album_id.value:
            album_id.error_text = "Album ID cannot be empty!"
            page.update()
        else:
            album_id_value = album_id.value
            album_results = get_album(album_id_value)
            album_tracks = []
            for rr in album_results['tracks']:
                album_tracks.append(TracksList(rr['name'], rr['artist'], rr['album'],
                                               rr['release_date'], rr['album_image'], page))
            t.tabs[1].clean()
            t.tabs[1].content = Column(
                controls=[
                    Container(
                        margin=10,
                        content=album_id
                    ),
                    ElevatedButton("Get Albums!", on_click=add_albums),
                    Row(controls=[
                        Image(
                            src=album_results['cover']
                        ),
                        Column(controls=[
                            Text(album_results['title'], size=40),
                            Text(f"Artists: {album_results['artists']}", size=25),
                            Text(f"Released On: {album_results['release_date']}", size=25)
                        ])
                    ]),
                    Column(controls=album_tracks)

                ], scroll=ScrollMode.ALWAYS
            )
            t.tabs[1].update()

    def get_top_10_artist_tracks(e):
        if not artist_id.value:
            artist_id.error_text = "Artist ID cannot be empty!"
            page.update()
        else:
            artist_id_value = artist_id.value
            artist_results = get_artist_top_10_tracks(artist_id_value)
            artist_tracks = []
            for rr in artist_results['tracks']:
                artist_tracks.append(TracksList(rr['name'], rr['artist'], rr['album'],
                                                rr['release_date'], rr['album_image'], page))
            t.tabs[2].clean()
            t.tabs[2].content = Column(
                controls=[
                    Container(
                        margin=10,
                        content=artist_id
                    ),
                    ElevatedButton("Get Top 10 Artist's Tracks!", on_click=get_top_10_artist_tracks),
                    Row(
                        controls=[
                            Image(
                                src=artist_results['artist_img']
                            ),
                            Column(
                                controls=[
                                    Text(artist_results['artist_name'], size=40),
                                    Text(f"Followers: {numerize.numerize(artist_results['followers'], 2)}", size=25),
                                    Text(f"Genres: {artist_results['genres']}", size=25)
                                ]
                            )
                        ]
                    ),
                    Column(controls=artist_tracks)

                ], scroll=ScrollMode.ALWAYS
            )
            t.tabs[2].update()

    def search_songs_button(e):
        if not song_search_name.value:
            song_search_name.error_text = "Song Name Cannot Be Empty!"
            page.update()
        else:
            song_search_name_value = song_search_name.value
            song_search_name_results = search_songs(song_search_name_value)
            song_search_name_tracks = []
            for rr in song_search_name_results:
                song_search_name_tracks.append(TracksList(rr['name'], rr['artist'], rr['album'],
                                                          "", rr['album_image'], page))
            t.tabs[3].clean()
            t.tabs[3].content = Column(
                controls=[
                    Container(
                        margin=10,
                        content=song_search_name
                    ),
                    ElevatedButton("Search Songs", on_click=search_songs_button),
                    Row(
                        controls=[
                            Column(
                                controls=[
                                    Text(f"Total Results: {len(song_search_name_tracks)}", size=40),
                                ]
                            )
                        ]
                    ),
                    Column(controls=song_search_name_tracks)

                ], scroll=ScrollMode.ALWAYS
            )
            t.tabs[3].update()

    t = Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            Tab(
                text="Spotify Playlist",
                content=Column(
                    controls=[
                        Container(
                            margin=10,
                            content=playlist_id
                        ),
                        ElevatedButton("Get Playlist!", on_click=add_playlist)
                    ]
                ),
            ),
            Tab(
                text="Spotify Albums",
                content=Column(
                    controls=[
                        Container(
                            margin=10,
                            content=album_id
                        ),
                        ElevatedButton("Get Albums!", on_click=add_albums)
                    ]
                ),
            ),
            Tab(
                text="Spotify Artist's Top 10 Songs",
                content=Column(
                    controls=[
                        Container(
                            margin=10,
                            content=artist_id
                        ),
                        ElevatedButton("Get Top 10 Artist's Tracks", on_click=get_top_10_artist_tracks)
                    ]
                ),
            ), Tab(
                text="Search Songs",
                content=Column(
                    controls=[
                        Container(
                            margin=10,
                            content=song_search_name
                        ),
                        ElevatedButton("Search Songs!", on_click=search_songs_button)
                    ]
                ),
            ),
        ],
        expand=1
    )

    page.add(t)


app(target=main)
