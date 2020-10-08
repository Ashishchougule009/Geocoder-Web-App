from flask import Flask, render_template,request, send_file
from geopy.geocoders import ArcGIS
import pandas
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success-table", methods=['POST'])
def success_table():
    global filename
    if request.method=="POST":
        file = request.files['file']
        try:
            df=pandas.read_csv(file)
            gc = ArcGIS()
            df["Coordinates"] =  df["Address"].apply(gc.geocode)
            df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x!=None else None)
            df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x!=None else None)
            df=df.drop("Coordinates",1)
            filename = datetime.datetime.now().strftime("uploads/%Y-%m-%d %H-%M-%S"+".csv")
            df.to_csv(filename,index=None)
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="Make sure you have an column named 'Address' in your file!!!")

@app.route('/download-file/')
def download():
    return send_file(filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__ =="__main__":
    app.debug = True
    app.run()