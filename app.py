from flask import Flask, render_template, request, send_file, url_for
import qrcode
import os

app = Flask(__name__, static_folder='static')

# Route for the main form page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle QR code generation
@app.route('/generate', methods=['POST'])
def generate_qr():
    data = ""

    # Collect text input
    if request.form.get('text'):
        data += request.form['text']

    # Collect social link input
    if request.form.get('social_link'):
        data += "\n" + request.form['social_link']

    # Handle image upload
    if request.files.get('image'):
        image_file = request.files['image']
        image_path = os.path.join('static', 'images', image_file.filename)
        image_file.save(image_path)
        
        # Generate image URL
        image_url = url_for('static', filename=f'images/{image_file.filename}')
        data += "\n" + request.host_url + image_url

    # Handle video upload
    if request.files.get('video'):
        video_file = request.files['video']
        video_path = os.path.join('static', 'videos', video_file.filename)
        video_file.save(video_path)
        
        # Generate video URL
        video_url = url_for('static', filename=f'videos/{video_file.filename}')
        data += "\n" + request.host_url + video_url

    # Generate QR code with collected data
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Save the generated QR code
    qr_code_path = os.path.join('static', 'qr_codes', 'qr_code.png')
    img.save(qr_code_path)

    # Send the generated QR code back to the user
    return send_file(qr_code_path, mimetype='image/png')

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/videos', exist_ok=True)
    os.makedirs('static/qr_codes', exist_ok=True)
    
    app.run(debug=True)
