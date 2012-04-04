# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import Image
import csv

app = Flask(__name__)
FILE_PATH = '/tmp/image'


#TODO descargar como CSV
#Ponerlo bonito en la web
#Meterle el login
#Meterle el plugin de tablesorter
#TODO Controlar el tamaño de los archivos
@app.route("/", methods=['GET', 'POST'])
def index():
    colours = ''
    if request.method == 'POST':
        f = request.files['image']
        f.save(FILE_PATH)
        im = Image.open('/tmp/image')
        colours = im.getcolors(im.size[0]*im.size[1])

    return render_template('index.html', colours=colours)


@app.route("/export")
def export():
    im = Image.open('/tmp/image')
    colours = im.getcolors(im.size[0]*im.size[1])
    f = open('result.csv', 'wb')
    colour_result = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for colour in colours:
        colour_result.writerow(colour)

    return f


if __name__ == "__main__":
    app.debug = True
    app.run()
