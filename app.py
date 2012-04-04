# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_from_directory
import Image
import csv

FILE_PATH = '/tmp/image'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#TODO descargar como CSV
#Ponerlo bonito en la web
#Meterle el login
#Meterle el plugin de tablesorter
#TODO Controlar el tamaño de los archivos
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    colours = ''
    if request.method == 'POST':
        f = request.files['image']

        if f and allowed_file(f.filename):
            f.save(FILE_PATH)
            im = Image.open('/tmp/image')
            colours = im.getcolors(im.size[0]*im.size[1])

    return render_template('index.html', colours=colours)


@app.route("/export")
def export():
    im = Image.open('/tmp/image')
    colours = im.getcolors(im.size[0]*im.size[1])
    f = open(app.config['UPLOAD_FOLDER'] + '/result.csv', 'wb')
    colour_result = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for colour in colours:
        colour_result.writerow(colour)
    f.close()

    return send_from_directory(app.config['UPLOAD_FOLDER'], 'result.csv')


if __name__ == "__main__":
    app.debug = True
    app.run()
