from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class MusicPlaylist:
    def __init__(self):
        self.date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
        self.top_100_endpoint = "https://www.billboard.com/charts/hot-100/"
        self.song_names = []

    def get_song_names(self):
        response = requests.get(url=self.top_100_endpoint + self.date)
        website_html = response.text
        soup = BeautifulSoup(website_html, "html.parser")
        song_name_spans = soup.select("li ul li h3")
        self.song_names = [song.get_text().strip() for song in song_name_spans]

    def create_spotify_playlist(self):
        client_id = "4b8528b5b7f0432d9fcd5f507011d6b3"
        client_secret = "4cc18076257c434388da1921924d0712"
        scope = "playlist-modify-public"
        user_name = "1232727695"
        redirect_uri = "http://example.com"
        token = SpotifyOAuth(scope=scope, username=user_name, client_id=client_id, client_secret=client_secret,
                             redirect_uri=redirect_uri)
        self.spotifyObject = spotipy.Spotify(auth_manager=token)

        playlist_name = f"Top 100 on {self.date}"
        playlist_description = f"These are the hottest songs from {self.date}"

        self.playlist = self.spotifyObject.user_playlist_create(user=user_name,
                                                                name=playlist_name,
                                                                public=True,
                                                                description=playlist_description)

    def add_songs_to_playlist(self):
        song_uri = []
        for song in self.song_names:
            results = self.spotifyObject.search(q=song)
            track_uri = results["tracks"]["items"][0]["uri"]
            song_uri.append(track_uri)

        self.spotifyObject.playlist_add_items(playlist_id=self.playlist["id"], items=song_uri)


if __name__ == "__main__":
    playlist_creator = MusicPlaylist()
    playlist_creator.get_song_names()
    playlist_creator.create_spotify_playlist()
    playlist_creator.add_songs_to_playlist()
