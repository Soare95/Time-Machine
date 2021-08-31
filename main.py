import request21
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/users"

user_date = input("What year you would like to travel to? (YYYY-MM-DD): ")
year = user_date.split("-")[0]

response_billboard = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}")
response_billboard.raise_for_status()
website = response_billboard.text
soup = BeautifulSoup(website, "html.parser")

all_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_titles = [item.getText() for item in all_songs]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True
                                               ))
user_id = sp.current_user()["id"]

uri_list = []
for song in song_titles:
    spotify_songs = sp.search(q=f"track: {song}, year: {year}", type="track")
    try:
        result = spotify_songs["tracks"]["items"][0]["uri"]
        uri_list.append(result)
    except IndexError:
        print(f"Song {song} doesn't exists on Spotify.")

create_playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
add_tracks = sp.playlist_add_items(playlist_id=create_playlist["id"], items=uri_list)

playlist = create_playlist["external_urls"]["spotify"]
print(f"You can see your playlist at: {playlist}")
