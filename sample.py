from flask import Flask, jsonify, request
from colorthief import ColorThief
import os, colorsys
from flask_cors import CORS
from flask import send_from_directory


proj = Flask(__name__)
CORS(proj, resources={r"/*": {"origins": "*"}})

U_FOLDER = "uimgs"
L_FOLDER = "limgs"
os.makedirs(U_FOLDER, exist_ok=True)
os.makedirs(L_FOLDER, exist_ok=True)

# ----- Helpers -----
def complementary_color(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    comp_h = (h + 0.5) % 1.0
    r2, g2, b2 = colorsys.hsv_to_rgb(comp_h, s, v)
    return tuple(int(x * 255) for x in (r2, g2, b2))

def rotate_hue(rgb, fraction):
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + fraction) % 1.0
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return (int(r2 * 255), int(g2 * 255), int(b2 * 255))

def analyze_image_colors(path):
    thief = ColorThief(path)
    dom = thief.get_color(quality=1)
    comp = complementary_color(dom)
    triadic = [rotate_hue(dom, 0.33), rotate_hue(dom, 0.66)]
    return {"dominant": dom, "complementary": comp, "triadic": triadic}

def color_distance(c1, c2):
    return sum((a-b)**2 for a,b in zip(c1, c2)) ** 0.5

# ----- Combined Route -----
@proj.route("/match", methods=["POST", "GET"])
def match_route():
    # ✅ POST → Upload and process
    if request.method == "POST":
        upper_imgs = request.files.getlist("uo")
        lower_imgs = request.files.getlist("lo")

        for img in upper_imgs:
            img.save(os.path.join(U_FOLDER, img.filename))
        for img in lower_imgs:
            img.save(os.path.join(L_FOLDER, img.filename))

        return jsonify({"message": "Images uploaded successfully!"})

    # ✅ GET → Perform matching and return combinations
    else:
        shirts, pants = [], []

        for file in os.listdir(U_FOLDER):
            colors = analyze_image_colors(os.path.join(U_FOLDER, file))
            shirts.append({"filename": file, **colors})

        for file in os.listdir(L_FOLDER):
            colors = analyze_image_colors(os.path.join(L_FOLDER, file))
            pants.append({"filename": file, "dominant": colors["dominant"]})

        combinations = []
        for shirt in shirts:
            best_match, best_dist = None, float("inf")
            for pant in pants:
                dist = color_distance(shirt["dominant"], pant["dominant"])
                if dist < best_dist:
                    best_match = pant
                    best_dist = dist
            if best_match:
                combinations.append({
                    "upper_url": f"/{U_FOLDER}/{shirt['filename']}",
                    "lower_url": f"/{L_FOLDER}/{best_match['filename']}"
                })

        return jsonify({"combinations": combinations})
    
@proj.route('/uimgs/<filename>')    
def serve_upper(filename):
     
    return send_from_directory(U_FOLDER, filename)

@proj.route('/limgs/<filename>')
def serve_lower(filename):
    return send_from_directory(L_FOLDER, filename)

if __name__ == "__main__":
    proj.run(debug=True)
