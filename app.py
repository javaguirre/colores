from flask import Flask, render_template, request
import Image

app = Flask(__name__)
FILE_PATH = '/tmp/image'

@app.route("/", methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        f = request.files['image']
        f.save(FILE_PATH)
        im = Image.open('/tmp/image')
#TODO descargar como CSV
#Ponerlo bonito en la web
#Meterle el login
        result = im.getcolors(im.size[0]*im.size[1])
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.debug = True
    app.run()
