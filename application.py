from flask import jsonify , Flask, render_template, request   
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

      genai.configure(api_key="AIzaSyDjaIlr4X50nCHRZyOsMLhdPPVaysToek8")
      model = genai.GenerativeModel("gemini-1.5-flash")
      response = model.generate_content(f)
      
      return render_template("uploaded.html" , response = response.text,question=f )  
      # return render_template("uploaded.html", display_detection = filename, fname = filename , detected_class = detected_class )      


@application.route("/getresponce" , methods = ['GET', 'POST'])
def generatetext():
   if request.method == 'POST':
    f = request.form['query']
    print(f)
    genai.configure(api_key="AIzaSyDjaIlr4X50nCHRZyOsMLhdPPVaysToek8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f)
    data = {
      "response" : response.text,
      "query" : f,
    }
    # print(response)
    return jsonify(data)

 
if __name__ == '__main__':
   application.run(port=4000, debug=True)
