import json
import ssl
import requests
import httplib, urllib, base64
import cognitive_face as CF

from flask import Flask, request
from flask_cors import CORS, cross_origin

from captionbot import CaptionBot

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '9b183b1c6508456aaa4bc24e0bcd4047',
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,facialHair,glasses',
})



KEY = '9b183b1c6508456aaa4bc24e0bcd4047'
CF.Key.set(KEY)

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

		r = {"success":caption}
		print "fff"
		linhas = getText(str(data))
		texto = ""
		if not linhas:
			print "Erro a ler texto na Imagem."
		else:
			texto = parseText(linhas)
		if texto:
		        aux = "this image has the following text: " + texto
		        response = {"success" : aux}
		        return json.dumps(response)
		#result = CF.face.detect(data)
		#print result
		try:
		    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
		    body = {"url":data}
		    conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
		    print("teste1")
		    response = conn.getresponse()
		    data = response.read()
		    #print(data)
		    data = json.loads(data)
		    if(data):
		    	#print(data[0]['faceId'])
		    	age = data[0]["faceAttributes"]["age"]
		    	gender = data[0]["faceAttributes"]["gender"]
		    	moustache = data[0]["faceAttributes"]["facialHair"]["moustache"]
		    	beard = data[0]["faceAttributes"]["facialHair"]["beard"]
		    	glasses = data[0]["faceAttributes"]["glasses"]
		    	print age 
		    	print gender
		    	print moustache
		    	print beard
		    	print glasses
		    	description = " It's gender is " + gender + " with an age of " + str(age) + " years. It has a "+str(100*float(moustache)) +" percent of having a moustache and "+str(100*float(beard))+" percent of having a beard. He has "+glasses
		    	r["success"] += description 

		    else:
		    	print "Face not found"

		    conn.close()
		except Exception as e:
		    print(e)

		return json.dumps(r)
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
