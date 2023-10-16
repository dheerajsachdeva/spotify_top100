from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("In what year do you want to travel(Format: YYYY-MM-DD): ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=URL)

soup = BeautifulSoup(response.text, "html.parser")
songs_name = soup.select("li ul li h3")
songs_list = [song.getText().strip() for song in songs_name]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                redirect_uri="http://example.com",
                                                client_id="7dfd70eedd1542fe9fa196644ba4e6c1",
                                                client_secret="60bc27cade6e49a584b2fdd4f784e9fb",
                                                show_dialog=True,
                                                cache_path="token.txt",
                                                username="dheeraj arya",
                                               )
                     )

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

