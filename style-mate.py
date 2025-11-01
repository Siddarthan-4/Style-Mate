from flask import Flask,jsonify,request
from colorthief import ColorThief
import os,colorsys

proj = Flask(__name__)

def complementary_color(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    comp_h = (h + 0.5) % 1.0  # 180° shift
    r2, g2, b2 = colorsys.hsv_to_rgb(comp_h, s, v)
    return tuple(int(x * 255) for x in (r2, g2, b2))

def rotate_hue(rgb, fraction):
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + fraction) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return (int(r2 * 255), int(g2 * 255), int(b2 * 255))

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
        comp=complementary_color(domcol)
        triadic = [rotate_hue(domcol, 0.33), rotate_hue(domcol, 0.66)]
        
        results1.append({
            "filename":img.filename,
            "dominant_color":domcol,
            "complementary_color":comp,
            "triadic":triadic
        })
        
    for img in lower_images:
        img_path2=os.path.join(f2,img.filename)
        img.save(img_path2)

        col=ColorThief(img_path2)
        domcol=col.get_color(quality=1)
        comp=complementary_color(domcol)
        triadic = [rotate_hue(domcol, 0.33), rotate_hue(domcol, 0.66)]
        
        results2.append({
            "filename":img.filename,
            "dominant_color":domcol,
            "complementary_color":comp,
            "triadic":triadic
        })

        return jsonify({
                        "upper images":results1,
                        "lower images":results2
                        }) 
    
if __name__ == '__main__':
    proj.run(debug=True)