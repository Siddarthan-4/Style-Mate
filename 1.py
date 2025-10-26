from flask import Flask,jsonify,request
from colorthief import ColorThief
import os

proj = Flask(__name__)

f1="uimgs"
f2="limgs"
os.makedirs(f1, exist_ok=True)
os.makedirs(f2, exist_ok=True)

@proj.route("/")
def home():
    return "home page"


@proj.route("/analyse",methods=["POST"])
def upload():
    results1=[]
    results2=[]

    upper_images=request.files.getlist("uo")
    lower_images=request.files.getlist("lo")

    for img in upper_images:
        img_path1=os.path.join(f1,img.filename)
        img.save(img_path1)

        col=ColorThief(img_path1)
        domcol=col.get_color(quality=1)

        results1.append({
            "filename":img.filename,
            "dominant_color":domcol
        })

    for img in lower_images:
        img_path2=os.path.join(f2,img.filename)
        img.save(img_path2)

        col=ColorThief(img_path2)
        domcol=col.get_color(quality=1)

        results2.append({
            "filename":img.filename,
            "dominant_color":domcol
        })

        return jsonify({
                        "upper images":results1,
                        "lower images":results2
                        }) 
    
if __name__ == '__main__':
    proj.run(debug=True)