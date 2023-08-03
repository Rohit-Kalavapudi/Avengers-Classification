from flask import Flask, request, jsonify
import util
import cv2
from flask_cors import CORS, cross_origin

app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/hello1',methods=['POST']) 
@cross_origin()
def hello1():
    util.load_saved_artifacts()
    a=request.json.get('data')
    a="data:image/jpeg;base64,"+a
    return jsonify(util.classify_image(a))

if(__name__ ) == "__main__":
    app.run(port=5000)
