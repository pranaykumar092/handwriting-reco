# ✍️ Handwriting Recognition App

An AI-powered handwriting recognition web application built with **Flask**, **EasyOCR**, **OpenCV**, and **TextBlob**. Upload an image of handwritten text, and the app will extract the text using deep learning-based OCR and automatically correct spelling errors.

---

## 🚀 Features

- **Handwriting to Text** — Upload a handwritten image and get extracted text instantly.
- **AI-Powered OCR** — Uses [EasyOCR](https://github.com/JaidedAI/EasyOCR) with deep learning models for accurate recognition.
- **Image Preprocessing** — Applies grayscale conversion, histogram equalization, Gaussian blur, Otsu thresholding, and morphological operations via OpenCV to improve OCR accuracy.
- **Spelling Correction** — Automatically corrects extracted text using [TextBlob](https://textblob.readthedocs.io/).
- **Clean Web Interface** — Responsive Bootstrap 5 UI with a modern gradient design.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Backend language |
| **Flask** | Web framework and routing |
| **EasyOCR** | Deep learning-based OCR for text extraction |
| **OpenCV** | Image preprocessing (blur, threshold, morphology) |
| **NumPy** | Numerical operations for image processing |
| **Pillow** | Image loading fallback |
| **TextBlob** | Spelling correction on extracted text |
| **Bootstrap 5** | Frontend styling and responsive layout |

---

## 📁 Project Structure

```
handwriting-reco/
├── app.py                 # Flask application (routes, OCR, spelling correction)
├── preprocess.py          # Image preprocessing pipeline (OpenCV)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── WORKFLOW.md            # Application architecture and data flow
├── templates/
│   └── index.html         # Frontend HTML template
└── static/
    ├── style.css          # Custom CSS styles
    └── uploads/           # Uploaded and processed images (created at runtime)
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pranaykumar092/handwriting-reco.git
   cd handwriting-reco
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in your browser:**
   ```
   http://127.0.0.1:5000
   ```

> **Note:** The first time you run the app, EasyOCR will automatically download the required language models (~100 MB). This only happens once.

---

## 📖 How to Use

1. Open the app in your browser at `http://127.0.0.1:5000`.
2. Click **"Select Image"** and choose a JPG or PNG image of handwritten text.
3. Click **"Recognize Handwriting"**.
4. View the **Extracted Text** (raw OCR output) and the **Corrected Text** (spelling-corrected version).
5. Compare the original and preprocessed images displayed below the text.

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 🙋 Author

**Pranay Kumar** — [GitHub Profile](https://github.com/pranaykumar092)