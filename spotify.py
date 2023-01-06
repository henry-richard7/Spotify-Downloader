import requests


def get_token():
    url = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
    r = requests.get(url).json()
    return r["accessToken"]


def get_playlist(playlist_id: str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {get_token()}"
    }
    response = requests.get(url, headers=headers).json()
    result = {
        "title": response['name'],
        "description": response['description'],
        "followers": response['followers']['total'],
        "cover": response['images'][0]['url']
    }
    tracks = []
    for track in response['tracks']['items']:
        tracks.append({
            "name": track["track"]['name'],
            "artist": ", ".join([x['name'] for x in track['track']['artists']]),
            "album": track['track']['album']['name'],
            "release_date": track['track']['album']['release_date'],
            "album_image": track['track']['album']['images'][0]['url']
        })
    result["tracks"] = tracks
    return result


def get_album(album_id: str):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = {
        "Authorization": f"Bearer {get_token()}"
    }
    response = requests.get(url, headers=headers).json()
    result = {
        "title": response['name'],
        "cover": response['images'][1]['url'],
        "artists": ", ".join(x['name'] for x in response['artists']),
        "release_date": response['release_date'],
    }
    tracks = []
    for track in response['tracks']['items']:
        tracks.append({
            "name": track['name'],
            "artist": ", ".join([x['name'] for x in track['artists']]),
            "album": response['name'],
            "album_image": response['images'][0]['url'],
            "release_date": response['release_date']
        })
    result["tracks"] = tracks
    return result


def get_artist_top_10_tracks(artist_id: str):
    url1 = f"https://api.spotify.com/v1/artists/{artist_id}"
    url2 = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=IN"
    headers = {
        "Authorization": f"Bearer {get_token()}"
    }

    response1 = requests.get(url1, headers=headers).json()

    result = {
        "artist_img": response1['images'][1]['url'],
        "artist_name": response1['name'],
        "followers": response1['followers']['total'],
        "genres": ", ".join(response1['genres'])
    }

    response2 = requests.get(url2, headers=headers).json()

    tracks = []
    for track in response2['tracks']:
        tracks.append({
            "name": track['name'],
            "artist": ", ".join([x['name'] for x in track['artists']]),
            "album": track['album']['name'],
            "release_date": track['album']['release_date'],
            "album_image": track['album']['images'][0]['url']
        })
    result['tracks'] = tracks
    return result
