from flask import Flask, render_template, request, redirect
import testSpotify
import requests

app = Flask(__name__)

app.artist = "default"
app.prev = ["default"]

@app.route("/")
def base():
	passArtist = app.artist
	print(passArtist)
	artistUrl = testSpotify.initArtist(passArtist)
	url = testSpotify.getUrl(artistUrl);
	track = testSpotify.getTrack(artistUrl);
	art = testSpotify.getAlbumArt(artistUrl);
	if(url == None):
		return redirect("/relatedArtist")

	
	if(app.artist != "default"):
		with open("download/song.mp3", "wb") as code:
			code.write(requests.get(url).content)
		return render_template('spot.html', pTrack=track, pUrl=url, pArt=art, pArtist=passArtist)
	else:
		return '''<body style="background:#383c4a;text-align:center;">
		<br>
		<br>
		<br>
		<div style="font-family:monospace;font-size:100px;color:aliceblue;font-weight:bold;">Spotify Controller</div>
		<br>
		<br>
		<br>
		<form method="POST" action="/updateArtist">
	<input type="form" style="height:42px;width:50%;font-family:monospace;font-size:25px;" name="artistForm"></input>
	<input type="submit" style="height:42px;width:35%;font-family:monospace;font-size:25px;" name="artistSubmit" value="Search for an Artist"></input>
	</form></body>'''
	
@app.route("/updateArtist", methods=['POST', 'GET'])
def form():
	if request.method == 'POST':
		app.artist = request.form["artistForm"]
		app.artist = app.artist.upper()
		app.prev = []
	return redirect("/")

@app.route("/relatedArtist")
def related():
	nextArtist = testSpotify.getRelatedArtist(app.artist)['artists'][0]['name']
	app.prev.append(app.artist)

	for i in range(0, 5):
		if(testSpotify.getRelatedArtist(app.artist)['artists'][i]['name'] not in app.prev):
			app.artist = testSpotify.getRelatedArtist(app.artist)['artists'][i]['name']
			break
	if(len(app.prev) >= 8):
		app.prev.clear()
	return redirect("/")	


if __name__ == '__main__':
	app.run()