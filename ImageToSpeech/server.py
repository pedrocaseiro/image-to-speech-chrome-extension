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

KEY = 'YOUR COGNITIVE FACE KEY HERE' #https://www.microsoft.com/cognitive-services/en-us/face-api
CF.Key.set(KEY)

app = Flask(__name__)
CORS(app)

visionAPI_key = "YOUR VISION API KEY HERE" #https://cloud.google.com/vision/

@app.route('/getDescription', methods=["GET", "POST"])
def getDescription():
    if request.method == "POST":
        img = request.data[5:]
        data = img
        c = CaptionBot()
        caption = c.url_caption(str(data))
        r = {"success":caption}
        lines = getText(str(data))
        text = ""
        if lines:
            text = parseText(lines)
            if text:
                response = {"success":text}
                return json.dumps(response)
            aux = "this image has the following text: " + text
            response = {"success" : aux}
            return json.dumps(response)
        try:
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            body = {"url":data}
            conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
            response = conn.getresponse()
            data = response.read()
            data = json.loads(data)
            if(data):
                age = data[0]["faceAttributes"]["age"]
                gender = data[0]["faceAttributes"]["gender"]
                moustache = data[0]["faceAttributes"]["facialHair"]["moustache"]
                beard = data[0]["faceAttributes"]["facialHair"]["beard"]
                glasses = data[0]["faceAttributes"]["glasses"]
                description = " It's gender is " + gender + " with an age of " + str(age) + " years. It has a "+str(100*float(moustache)) +" percent probability of having a moustache and "+str(100*float(beard))+" percent probability of having a beard. He has "+glasses
                r["success"] += description 
            conn.close()
        except Exception as e:
            print(e)
        return json.dumps(r)

# Restrictions: <4MB | JPEG, PNG, GIF, BMP | min:40x40 max:3200x3200 px
def getText(img_link):
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
    regions = []
    if response.status_code == 200:
        regions = response.json()['regions']
        return regions	

def parseText(lines):
    aux = lines[0]["lines"]
    final_text = "This image contains the following text: "
    for l in aux:
        for w in l["words"]:
            final_text = final_text + " " + w["text"]
            return final_text


if __name__ == '__main__':
    context = ('ca.crt', 'ca.key')
    app.run(host= '0.0.0.0',port=5000, ssl_context=context)
