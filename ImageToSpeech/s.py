import json
import ssl
import requests
import httplib, urllib, base64
from flask import Flask, request
from flask_cors import CORS, cross_origin

from captionbot import CaptionBot

app = Flask(__name__)
CORS(app)

visionAPI_key = "eb752fbad1dc4cdcbd3943e372ddd6e0"

@app.route('/getDescription', methods=["GET", "POST"])
def getDescription():
	if request.method == "POST":
		img = request.data[5:]
		print img
		data = img
		c = CaptionBot()
		caption = c.url_caption(str(data))
	    
		response = {"success":caption}
		print "fff"
		linhas = getText(str(data))
		texto = ""
		if not linhas:
			print "Erro a ler texto na Imagem."
		else:
			texto = parseText(linhas)
		if texto:
			print texto
		return json.dumps(response)
	else:
		print "Hello World"


# Restricoes: <4MB | JPEG, PNG, GIF, BMP | min:40x40 max:3200x3200 px
def getText(img_link):
	print "## OCR ##"
	requestBody = json.dumps({"url":str(img_link)})
	headers = {
    	# Request headers
    	'Content-Type': 'application/json',
    	'Ocp-Apim-Subscription-Key': visionAPI_key,
	}
	params = urllib.urlencode({
    	# Request parameters
    	'language': 'unk',
    	'detectOrientation ': 'true',
	})
	response = requests.post("https://westus.api.cognitive.microsoft.com/vision/v1.0/ocr", data=requestBody, params=params, headers=headers)
	print response.text
	regions = []
	if response.status_code == 200:
		regions = response.json()['regions']
	return regions	


# Lista com dicts
def parseText(lines):
	linhas = lines[0]["lines"]
	texto_final = ""
	for l in linhas:
		for w in l["words"]:
			texto_final = texto_final + " " + w["text"]
	return texto_final


if __name__ == '__main__':
    context = ('ca.crt', 'ca.key')
    app.run(host= '0.0.0.0',port=5000, ssl_context=context)
