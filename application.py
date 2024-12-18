from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import json
# from PIL import Image
import os
import google.generativeai as genai
import re




application = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@application.route("/")
def index():
  return render_template("index.html")

@application.route("/about")
def about():
  return render_template("about.html")

@application.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.form['file']
      print(f)

      genai.configure(api_key="IzaSyDjaIlr4X50nCHRZyOsMLhdPPVaysToek8")
      model = genai.GenerativeModel("gemini-1.5-flash")
      response = model.generate_content(f)
      
      return render_template("uploaded.html" , response = response.text,question=f )  
      # return render_template("uploaded.html", display_detection = filename, fname = filename , detected_class = detected_class )      


def convert_to_json(data):
 
        # Assuming data is a list of tuples in the format (class, conf, [x, y, x1, y1])
        json_list = []
        for item in data:
            class_name, confidence, coordinates = item
            json_list.append({"class": class_name, "confidence": confidence, "coordinates":{
                    "xmin": coordinates[0],
                    "ymin": coordinates[1],
                    "xmax": coordinates[2],
                    "ymax": coordinates[3]
                }})
            
        # Convert list to JSON string
        json_data = json.dumps(json_list)
        return json_data

    


@application.route('/detector', methods = ['POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      # create a secure filename
      filename = secure_filename(f.filename)
      print(filename)
      # save file to /static/uploads
      filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
      print(filepath)
      f.save(filepath)
      
      detected_class = get_image(filepath, filename)
      print(detected_class)
      json_data = convert_to_json(detected_class)
      print(json_data)
      
      return json_data


if __name__ == '__main__':
   application.run(port=4000, debug=True)
