
# Brain Tumor Detection System

A web-based application for AI-powered brain tumor detection from medical images. The system features a modern frontend and a Flask backend serving a deep learning model for image analysis. **This project uses the dataset provided in the `braimer-main` directory for model training and analysis.**

## Features
- **AI-Powered Detection:** Uses a trained Keras model (`effnet.h5`) to classify brain MRI images as Glioma Tumor, Meningioma Tumor, Pituitary Tumor, or No Tumor.
- **User-Friendly Interface:** Responsive frontend with dark/light mode, animated UI, and easy navigation.
- **Fast Processing:** Upload an image and get results in seconds.
- **History Tracking:** View analysis history in the dashboard.
- **Demo Login:** Simple login system for demonstration purposes.
- **Doctor Recommendations:** Get specialist doctor suggestions by city.
- **Profile Management:** User profile page for managing account details.

## Project Structure
```
app.py                # Flask backend server
requirements.txt      # Python dependencies
effnet.h5             # Trained Keras model
unet-e012d006.pt      # (If used) Additional model file
frontend/             # Frontend static files
  ├── index.html      # Home page
  ├── dashboard.html  # Image upload & results
  ├── login.html      # Login page
  ├── about.html      # About page
  ├── services.html   # Services page
  ├── contact.html    # Contact page
  ├── doctors.html    # Doctor recommendations
  ├── profile.html    # User profile page
  ├── script.js       # Frontend logic
  └── styles.css      # Stylesheet
LICENSE               # Project license
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation
1. **Clone the repository:**
   ```powershell
   git clone <this-repo-url>
   cd braimer-deploy
   ```
2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Ensure the model file is present:**
   - Place `effnet.h5` in the project root (same directory as `app.py`).

### Running the Application
1. **Start the backend server:**
   ```powershell
   python app.py
   ```
   The server will run at `http://127.0.0.1:5000/` by default.

2. **Open the frontend:**
   - Open `frontend/index.html` in your browser, or
   - Serve the `frontend/` folder using a simple HTTP server (for full functionality with API calls):
     ```powershell
     cd frontend
     python -m http.server 8000
     ```
   - Visit `http://localhost:8000/` in your browser.

### Demo Login
- **Email:** `test@example.com`
- **Password:** `password`

## Usage
1. Login via the login page.
2. Upload a brain MRI image in the dashboard.
3. View the AI's prediction, analysis history, and doctor recommendations.
4. Manage your profile via the profile page.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements
- Built with [Flask](https://flask.palletsprojects.com/) and [TensorFlow/Keras](https://www.tensorflow.org/).
- Frontend uses [Poppins](https://fonts.google.com/specimen/Poppins) font and modern CSS.
=======
