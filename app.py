from flask import Flask, render_template, request, url_for, send_file
import qrcode
from urllib.parse import urlparse
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def generate_qrcode():
    if request.method == 'POST':
        url = request.form['url']
        try:
            parsed_url = urlparse(url)
            if not bool(parsed_url.scheme) or not bool(parsed_url.netloc):
                error_message = "Invalid URL. Please enter a valid website address."
            else:
                error_message = None 
        except ValueError:
            error_message = "Invalid URL format. Please enter a valid website address."

        if error_message:
            return render_template('qr_code.html', error=error_message)

        with tempfile.NamedTemporaryFile(suffix=".png", dir=app.config['TEMP_DIR'], delete=False) as temp_file:
            filename = os.path.basename(temp_file.name)  # Get the filename without full path

            features = qrcode.QRCode(version=1, box_size=40, border=3)
            features.add_data(url)
            features.make(fit=True)
            gen_img = features.make_image(fill_color="black", back_color="white")
            gen_img.save(temp_file.name)
        return send_file(os.path.join(app.config['TEMP_DIR'], filename), mimetype='image/png')

        return render_template('qr_code.html', qr_image_path=filename)
    

    return render_template('index.html')

if __name__ == '__main__':
    app.config['TEMP_DIR'] = os.path.join(os.getcwd(), 'temp')
    app.run(debug=True)
