from flask import Flask, request, render_template_string, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from fpdf import FPDF
from io import BytesIO
from datetime import timedelta
import base64

app = Flask(__name__)
app.secret_key = 'secret123'

app.permanent_session_lifetime = timedelta(days=7)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = tf.keras.models.load_model(r"C:\Users\anupa\OneDrive\Desktop\SkinCancerApp\model.keras")

class_names = [
    "Actinic Keratoses",
    "Basal Cell Carcinoma",
    "Benign Keratosis-like Lesions",
    "Dermatofibroma",
    "Melanocytic Nevi",
    "Melanoma",
    "Vascular Lesions"
]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

user_data = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

HTML_TEMPLATE = """
<!DOCTYPE html>

<html>
<head>
    <title>Skin Cancer Detection</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #fff6f6, #f9e7ff, #e0f7fa, #e1ffe1);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .box {
            background: white;
            padding: 2rem;
            border-radius: 1.5rem;
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
            width: 90%;
            max-width: 500px;
        }

        h2 {
            text-align: center;
            color: #2c3e50;
        }

        input, select, button {
            width: 100%;
            padding: 12px;
            margin-bottom: 1rem;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 1rem;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
        }

        .checkbox-group input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
        }

        button {
            background: #ff6b6b;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        button:hover {
            background: #ff4757;
            transform: scale(1.05);
        }

        .logout {
            text-align: center;
            margin-top: 1rem;
        }

        a {
            color: #2980b9;
            text-decoration: none;
        }

        a:hover {
            color: #3498db;
        }

        p {
            text-align: center;
            font-weight: bold;
            color: #e67e22;
        }

        .preview-img {
            display: block;
            max-width: 100%;
            max-height: 300px;
            margin: 20px auto;
            border-radius: 1rem;
            border: 3px solid #ddd;
        }
    </style>
</head>
<body>
<div class="box">
    <h2>{{ title }}</h2>
    {% if message %}<p>{{ message }}</p>{% endif %}
    <form method="POST" enctype="multipart/form-data">
        {% if title == "Register" %}
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <input type="text" name="name" placeholder="Full Name" required />
            <input type="text" name="age" placeholder="Age" required />
            <select name="sex" required>
                <option value="" disabled selected>Select Sex</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
            <input type="email" name="email" placeholder="Email" required />
            <input type="text" name="phone" placeholder="Phone Number" required />
            <button type="submit">Register</button>
            <div class="logout">Already registered? <a href="/login">Login</a></div>
        {% elif title == "Login" %}
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <div class="checkbox-group">
                <input type="checkbox" name="remember" id="remember">
                <label for="remember">Remember Me</label>
            </div>
            <button type="submit">Login</button>
            <div class="logout">New user? <a href="/register">Register</a></div>
        {% else %}
            <input type="file" name="file" required />
            <button type="submit">Upload and Predict</button>
            {% if prediction %}
                <p><strong>Prediction:</strong> {{ prediction }}</p>
            {% endif %}
            {% if image_base64 %}
                <img src="data:image/jpeg;base64,{{ image_base64 }}" class="preview-img" />
            {% endif %}
            {% if session.username %}
                <div class="logout"><a href="/report">Download PDF Report</a> | <a href="/logout">Logout</a></div>
            {% endif %}
        {% endif %}
    </form>
</div>
</body>
</html>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username in user_data:
            return render_template_string(HTML_TEMPLATE, title="Register", message="Username already exists.")
        user_data[username] = {
            'password': request.form['password'],
            'name': request.form['name'],
            'age': request.form['age'],
            'sex': request.form['sex'],
            'email': request.form['email'],
            'phone': request.form['phone']
        }
        return redirect(url_for('login'))
    return render_template_string(HTML_TEMPLATE, title="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        if username in user_data and user_data[username]['password'] == password:
            session['username'] = username
            session.permanent = bool(remember)
            return redirect(url_for('upload'))
        else:
            return render_template_string(HTML_TEMPLATE, title="Login", message="Invalid credentials.")
    return render_template_string(HTML_TEMPLATE, title="Login")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    prediction = None
    image_base64 = None

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            session['last_image'] = filepath

            image = preprocess_image(filepath)
            preds = model.predict(image)[0]
            top_class = np.argmax(preds)
            predicted_label = class_names[top_class]

            session['prediction'] = predicted_label
            prediction = predicted_label
            image_base64 = image_to_base64(filepath)

    return render_template_string(
        HTML_TEMPLATE,
        title="Upload",
        prediction=prediction,
        image_base64=image_base64
    )

@app.route('/report')
def report():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = user_data[session['username']]
    image_path = session.get('last_image')
    prediction = session.get('prediction', 'N/A')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Skin Cancer Detection Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {user['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {user['age']}", ln=True)
    pdf.cell(200, 10, txt=f"Sex: {user['sex']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {user['email']}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {user['phone']}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Prediction: {prediction}", ln=True)

    if image_path and os.path.exists(image_path):
        pdf.image(image_path, x=50, y=100, w=100)

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return send_file(
        pdf_output,
        as_attachment=True,
        download_name='SkinCancerReport.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
