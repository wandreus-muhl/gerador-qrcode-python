from flask import Flask, render_template, redirect, url_for, request, send_file
from werkzeug.utils import secure_filename
import qrcode, os, uuid, sys

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        url = request.form["inputURL"]

        qr = qrcode.QRCode(
            version=10,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        if request.form.get("geracaoMassa"):
            aux = url.split(";")
            print(aux, file=sys.stderr)
            for c in aux:
                a = c.split(":")
                print(a, file=sys.stderr)

                qr.filename = a[0] + ".png"
                qr.add_data(a[1])
                qr.make()
                image = qr.make_image()

                pasta = "./app/qrcodes/"
                image.save(os.path.join(pasta, secure_filename(qr.filename)))
                qr.clear()

        if not request.form.get("geracaoMassa"):
            qr.add_data(url)
            qr.make()
            qr.filename = str(uuid.uuid4()) + ".png"

            image = qr.make_image()

            pasta = "./app/qrcodes/"
            image.save(os.path.join(pasta, secure_filename(qr.filename)))

    return render_template("index.html")
