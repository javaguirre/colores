from flask import Flask, render_template, request
import Image
import csv

app = Flask(__name__)
FILE_PATH = '/tmp/image'

@app.route("/", methods=['GET', 'POST'])
def index():
    colours = ''
    if request.method == 'POST':
        f = request.files['image']
        f.save(FILE_PATH)
        im = Image.open('/tmp/image')
#TODO descargar como CSV
#Ponerlo bonito en la web
#Meterle el login
#Meterle el plugin de tablesorter
        colours = im.getcolors(im.size[0]*im.size[1])
        color_result = csv.writer(open('result.csv', 'wb'), delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for colour in colours:
            color_result.writerow(colour)

    return render_template('index.html', colours=colours)

if __name__ == "__main__":
    app.debug = True
    app.run()
