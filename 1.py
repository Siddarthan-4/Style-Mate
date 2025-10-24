from flask import Flask,jsonify,request
from colorthief import ColorThief
import os

proj = Flask(__name__)

folder="imgs"
os.makedirs(folder, exist_ok=True)

@proj.route("/")
def home():
    return "home page"


@proj.route("/analyse",methods=["POST"])
def upload():
    results=[]

    images=request.files.getlist("file")
    for img in images:
        img_path=os.path.join(folder,img.filename)
        img.save(img_path)

        col=ColorThief(img_path)
        domcol=col.get_color(quality=1)

        results.append({
            "filename":img.filename,
            "dominant_color":domcol
        })

    return jsonify({"files":results})

if __name__ == '__main__':
    proj.run(debug=True)