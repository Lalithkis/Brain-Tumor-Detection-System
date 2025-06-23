<h1 align="center">🧠 Braimer</h1>
<p align="center">
  <b>AI-Powered Brain Tumor Detection System</b><br>
  <i>Fast, accurate, and user-friendly MRI analysis for medical professionals and researchers.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-green?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange?logo=html5" alt="Frontend">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?logo=open-source-initiative" alt="License">
</p>

---

## ✨ Features

- <b>Accurate Detection</b>: Deep learning for reliable brain tumor identification
- <b>Real-Time Analysis</b>: Instant results via a modern web interface
- <b>No Installation</b>: Just open the frontend in your browser
- <b>Organized Datasets</b>: Easy-to-use train/test data folders
- <b>Extensible</b>: Ready for research, clinical, or educational use

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```text
brain-tumor-detection/
├── backend/            # Backend code (Python/Flask)
│   ├── backend.py      # Flask server application
│   ├── model/          # Saved machine learning models
│   │   └── <your_model>.h5 or other model file
│   ├── utils/          # Utility functions
│   │   └── <preprocessing.py, other custom scripts>
│   └── requirements.txt # Required Python libraries
│   
├── data/               # Place to keep image and other related datasets
│   ├── test/           # Place for storing test datasets
│   └── train/          # Place for training datasets
│
├── frontend/           # Frontend code
│   ├── index.html      # User interface main file
│   ├── styles.css      # CSS for design
│   ├── script.js       # Frontend scripting
│   └── assets/         # UI assets (images, etc.)
│
├── docs/               # Documentation files
│   └── README.md
│
├── .gitignore          # Specifies intentionally untracked files
│
└── requirements_dev.txt # Requirements to run dev tools
```
</details>

### Key Structure Points
- <b>Backend</b>: Flask server, ML model, and utilities
- <b>Frontend</b>: HTML/CSS/JS for user interaction
- <b>Data</b>: Separate folders for training and testing

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git

### Backend Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/gkrishna247/braimer.git
    cd braimer
    ```
2. Set up the backend:
    ```sh
    cd backend
    pip install -r requirements.txt
    ```
3. (Optional) Set environment variables as needed.
4. Start the Flask server:
    ```sh
    python backend.py
    ```
    The server runs at <a href="http://127.0.0.1:5000/" target="_blank">http://127.0.0.1:5000/</a> by default.

### Frontend Setup
- No installation required. Open <code>frontend/index.html</code> in your browser.
- Ensure the backend server is running for predictions.

---

## 🖼️ Usage

1. Open the web interface (<code>frontend/index.html</code>).
2. Upload an MRI image.
3. Click <b>Analyze</b>. The result will be displayed after processing.

---

## 🤝 Contribution

We encourage you to contribute! Please open an issue before making large changes.

---

## 📧 Contact

For questions or support, email: <a href="mailto:krishnamoorthitech2224@gmail.com@gmail.com">krishnamoorthitech2224@gmail.com</a>

---

## 📄 License

This project is licensed under the terms of the <code>LICENSE</code> file in this repository.