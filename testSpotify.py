import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials("772a83f4ee434fe3bbae2aebc2a22c58", "90caf81062c84720a780d4b0e0cf2acc")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def initArtist(artistName):
	name = artistName
	link = sp.search(q='artist:' + name, type='artist')['artists']['items'][0]['id']
	artistUrl = 'spotify:artist:' + link
	return artistUrl

def getTrack(artistUrl):	
	results = sp.artist_top_tracks(artistUrl)
	return results['tracks'][0]['name']

def getUrl(artistUrl):	
	results = sp.artist_top_tracks(artistUrl)
	return results['tracks'][0]['preview_url']

def getAlbumArt(artistUrl):	
	results = sp.artist_top_tracks(artistUrl)
	return results['tracks'][0]['album']['images'][0]['url']

def getRelatedArtist(name):
	artistUrl = sp.search(q='artist:' + name, type='artist')['artists']['items'][0]['id']
	print(artistUrl)
	return sp.artist_related_artists(artistUrl)
