import json
import ssl
from flask import Flask, request
from flask_cors import CORS, cross_origin

from captionbot import CaptionBot


app = Flask(__name__)
CORS(app)

@app.route('/getDescription', methods=["GET", "POST"])
def getDescription():
	if request.method == "POST":
		img = request.data[5:]
		print img
		data = img
		c = CaptionBot()
		text = c.url_caption(str(data))
	    
		response = {"success":text}
		print "fff"
		return json.dumps(response)
    
#js = json.dumps("mensagem")
#resp = Response(js, status=200, mimetype='application/json')

    


if __name__ == '__main__':
    context = ('ca.crt', 'ca.key')
    app.run(host= '0.0.0.0',port=5000, ssl_context=context, debug=True)