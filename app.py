from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
import io
import os
import cv2 # For OpenCV operations
import tensorflow as tf # For loading and using the Keras model
import random # Add this import
import base64
from fpdf import FPDF
import tempfile
import smtplib
from email.message import EmailMessage
import ssl

app = Flask(__name__)
CORS(app)

# --- Model Loading ---
MODEL_LOAD_PATH = 'effnet.h5' # Make sure this file is in the same directory or provide the correct path
loaded_model = None

try:
    if os.path.exists(MODEL_LOAD_PATH):
        loaded_model = tf.keras.models.load_model(MODEL_LOAD_PATH)
        print(f"Model '{MODEL_LOAD_PATH}' loaded successfully.")
    else:
        print(f"Error: Model file not found at '{MODEL_LOAD_PATH}'. The /analyze endpoint will not work.")
except Exception as e:
    print(f"Error loading Keras model: {e}")
    # loaded_model will remain None, and we can check for this in the analyze route

# --- Segmentation Model Loading ---
SEG_MODEL_PATH = 'unet-e012d006.pt'
segmentation_model = None

try:
    import torch
    segmentation_model = torch.hub.load('mateuszbuda/brain-segmentation-pytorch', 'unet',
        in_channels=3, out_channels=1, init_features=32, pretrained=True)
    segmentation_model.eval()
    print("Segmentation model loaded from torch.hub successfully.")
except Exception as e:
    print(f"Error loading segmentation model: {e}")
    # segmentation_model will remain None

# Dummy user database (replace with a real database in production)
users = {
    "test@example.com": {"password": "password", "name": "Test User"}
}

@app.route('/', methods=['GET'])
def homepage():
    """Simple homepage to test server connection."""
    return '<h2>Braimer Deploy Server is running.</h2>', 200

@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = users.get(email) # Get user data

    if user and user['password'] == password: # Check if user exists and password matches
        # Generate a dummy session token
        session_token = f"dummy_token_for_{email.split('@')[0]}_{random.randint(10000, 99999)}"
        user_name = user.get('name', 'User') # Get user's name, default to 'User'
        return jsonify({
            'message': 'Login successful',
            'session_token': session_token,
            'user_name': user_name
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"message": "Missing email, password, or name"}), 400

    # Basic type validation
    if not isinstance(email, str) or not isinstance(password, str) or not isinstance(name, str):
        return jsonify({"message": "Email, password, and name must be strings"}), 400

    if len(password) < 6: # Basic password length check
        return jsonify({"message": "Password must be at least 6 characters long"}), 400

    if email in users:
        return jsonify({"message": "Email already registered"}), 409 # Conflict

    # In a real app, hash the password before storing:
    # from werkzeug.security import generate_password_hash
    # users[email] = {"password": generate_password_hash(password), "name": name}
    users[email] = {"password": password, "name": name}

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/analyze', methods=['POST'])
def analyze_image_endpoint(): # Renamed to avoid conflict with PIL.Image
    """
    Handles image analysis request from the frontend.
    Returns:
        json: the analysis result.
    """
    if loaded_model is None:
        return jsonify({"error": "AI Model not loaded on the server. Cannot perform analysis."}), 503 # Service Unavailable

    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']
        city = request.form.get('city', '').strip().lower()  # Accept city from form-data

        # Open the image using Pillow
        pil_image = Image.open(io.BytesIO(image_file.read()))

        # Preprocess image for the model
        preprocessed_image_array = preprocess_for_model(pil_image)

        # Run prediction
        prediction_result = run_model_prediction(preprocessed_image_array)

        # Highlight tumor area if tumor detected
        # (Highlighting feature removed as per request)
        prediction_result['highlighted_image_base64'] = None

        # Add doctor recommendations
        prediction_result['doctor_recommendations'] = get_doctor_recommendations(city)

        return jsonify(prediction_result), 200 # prediction_result is already a dict

    except Exception as e:
        print(f"Error during analysis: {e}")
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """
    Generate a PDF report for the analysis and return it for download.
    Expects JSON with keys: prediction_label, confidence_score, datetime, highlighted_image_base64, original_image_base64
    """
    data = request.get_json()
    prediction_label = data.get('prediction_label', 'N/A')
    confidence_score = data.get('confidence_score', 'N/A')
    scan_datetime = data.get('datetime', 'N/A')
    highlighted_image_base64 = data.get('highlighted_image_base64')
    original_image_base64 = data.get('original_image_base64')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Brain Tumor Detection Report', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Date & Time: {scan_datetime}', ln=True)
    pdf.cell(0, 10, f'Prediction: {prediction_label}', ln=True)
    pdf.cell(0, 10, f'Confidence Score: {confidence_score}%', ln=True)
    pdf.ln(5)
    if original_image_base64:
        img_path = tempfile.mktemp(suffix='.jpg')
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(original_image_base64))
        pdf.cell(0, 10, 'Uploaded Image:', ln=True)
        pdf.image(img_path, w=80)
        pdf.ln(5)
    if highlighted_image_base64:
        img_path2 = tempfile.mktemp(suffix='.jpg')
        with open(img_path2, 'wb') as f:
            f.write(base64.b64decode(highlighted_image_base64))
        pdf.cell(0, 10, 'Tumor Highlighted Image:', ln=True)
        pdf.image(img_path2, w=80)
        pdf.ln(5)
    pdf_path = tempfile.mktemp(suffix='.pdf')
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True, download_name='BrainTumorReport.pdf')

@app.route('/email_report', methods=['POST'])
def email_report():
    """
    Email the PDF report to a doctor/hospital.
    Expects JSON with keys: to_email, subject, body, report_pdf_base64
    """
    data = request.get_json()
    to_email = data.get('to_email')
    subject = data.get('subject', 'Brain Tumor Detection Report')
    body = data.get('body', '')
    report_pdf_base64 = data.get('report_pdf_base64')
    if not (to_email and report_pdf_base64):
        return jsonify({'error': 'Missing recipient email or report PDF'}), 400
    # Save PDF to temp file
    pdf_path = tempfile.mktemp(suffix='.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(base64.b64decode(report_pdf_base64))
    # Email config (replace with your SMTP server details)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_user = 'your_email@gmail.com'  # Replace with your email
    smtp_pass = 'your_app_password'     # Replace with your app password
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg.set_content(body)
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename='BrainTumorReport.pdf')
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return jsonify({'message': 'Report emailed successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

def preprocess_for_model(pil_img):
    """
    Preprocesses the PIL image for the effnet.h5 model.
    Args:
        pil_img (PIL.Image): The input image.
    Returns:
        numpy.ndarray: The preprocessed image array.
    """
    # Convert PIL Image to NumPy array
    img_array = np.array(pil_img)

    # If the image is RGBA or Grayscale, convert to RGB
    if img_array.ndim == 2: # Grayscale
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4: # RGBA
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    # Convert RGB (from PIL) to BGR (for OpenCV and potentially the model)
    opencv_image_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Resize to model's expected input size
    img_resized = cv2.resize(opencv_image_bgr, (150, 150))
    
    # Reshape for the model: (batch_size, height, width, channels)
    img_reshaped = img_resized.reshape(1, 150, 150, 3)
    
    # Normalization: The original Jupyter code doesn't show explicit normalization (e.g. /255.0)
    # before model.predict(). If your 'effnet.h5' model was trained on pixel values
    # in the range [0, 255], then no normalization is needed here.
    # If it was trained on [0, 1] or [-1, 1], you'd add:
    # img_reshaped = img_reshaped / 255.0  # For [0,1]
    # Or use tf.keras.applications.efficientnet.preprocess_input if it's a standard EfficientNet

    return img_reshaped

def run_model_prediction(image_array):
    """
    Runs prediction using the loaded Keras model and maps output to labels.
    Args:
        image_array (numpy.ndarray): The preprocessed image array.
    Returns:
        dict: A dictionary containing the prediction label, class, and confidence score.
    """
    if loaded_model is None: # Should be checked before calling, but as a safeguard
        raise RuntimeError("Model is not loaded.")

    prediction_probabilities = loaded_model.predict(image_array)
    predicted_class_index = np.argmax(prediction_probabilities, axis=1)[0]
    confidence_score = float(np.max(prediction_probabilities))  # Get the highest probability

    prediction_label = ""
    has_tumor = False # Default, will be overridden if a tumor is detected

    if predicted_class_index == 0:
        prediction_label = 'Glioma Tumor'
        has_tumor = True
    elif predicted_class_index == 1:
        prediction_label = 'No Tumor' # This means no tumor detected by the model
        has_tumor = False
    elif predicted_class_index == 2:
        prediction_label = 'Meningioma Tumor'
        has_tumor = True
    else: # Assuming class 3 for 'Pituitary Tumor'
        prediction_label = 'Pituitary Tumor'
        has_tumor = True

    confidence_percent = round(confidence_score * 100, 2)
    message = f"The model predicts: {prediction_label} with {confidence_percent}% confidence"

    return {
        "predicted_class_index": int(predicted_class_index), # Send as int
        "prediction_label": prediction_label,
        "has_tumor": has_tumor,
        "confidence_score": confidence_percent,
        "message": message
    }

def highlight_tumor_area(image_bgr, tumor_class_index):
    """
    (Highlighting feature removed. This function is now a no-op.)
    """
    return image_bgr

def get_doctor_recommendations(city):
    """
    Returns a list of specialist doctors for the given city.
    Args:
        city (str): City name (lowercase)
    Returns:
        list: List of doctor dicts
    """
    doctors_by_city = {
        'salem': [
            {'name': 'Dr. S. Kumar', 'specialty': 'Neurosurgeon', 'hospital': 'Salem Neuro Center', 'contact': '+91-9876543210'},
            {'name': 'Dr. Priya R.', 'specialty': 'Oncologist', 'hospital': 'Salem Oncology Clinic', 'contact': '+91-9123456780'},
        ],
        'chennai': [
            {'name': 'Dr. A. Srinivasan', 'specialty': 'Neurosurgeon', 'hospital': 'Apollo Hospitals', 'contact': '+91-9000000001'},
            {'name': 'Dr. Meena S.', 'specialty': 'Oncologist', 'hospital': 'MIOT International', 'contact': '+91-9000000002'},
        ],
        'coimbatore': [
            {'name': 'Dr. R. Balaji', 'specialty': 'Neurosurgeon', 'hospital': 'CBE Brain & Spine', 'contact': '+91-9000000003'},
            {'name': 'Dr. Latha V.', 'specialty': 'Oncologist', 'hospital': 'Ganga Hospital', 'contact': '+91-9000000004'},
        ],
    }
    return doctors_by_city.get(city, [])

if __name__ == '__main__':
    # Make sure 'effnet.h5' is in the same directory as this script,
    # or update MODEL_LOAD_PATH.
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False) # use_reloader=False is good when loading models once