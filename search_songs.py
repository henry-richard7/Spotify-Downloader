from ytmusicapi import YTMusic


def search_songs(name):
    ytmusic = YTMusic()
    results = ytmusic.search(f"{name}", "songs")
    results_ = []
    for i in results:
        results_.append({
            "name": i['title'],
            "artist": ", ".join(x['name'] for x in i['artists']),
            "album": i['album']['name'],
            "album_image": i['thumbnails'][0]['url'].replace('w60-h60', 'w500-h500')
        })
    return results_
