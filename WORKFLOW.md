# 🔄 Application Workflow & Architecture

This document explains the end-to-end flow of the **Handwriting Recognition App**, from image upload to text extraction and correction.

---

## High-Level Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend   │────▶│  Flask Backend   │────▶│  Image Saved to │
│  (Browser)   │     │    (app.py)      │     │  static/uploads/ │
└──────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  preprocess.py   │
                     │  (OpenCV)        │
                     │  Grayscale,      │
                     │  Blur, Threshold │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │    EasyOCR       │
                     │  Text Extraction │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │    TextBlob      │
                     │  Spelling Fix    │
                     └──────────────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │  JSON Response   │──────▶  Frontend displays
                     │  to Browser      │         extracted + corrected text
                     └──────────────────┘
```

---

## Step-by-Step Flow

### 1. User Uploads an Image (Frontend)

- The user opens `http://127.0.0.1:5000` in their browser.
- The Flask app serves `templates/index.html`, which provides a file upload form.
- The user selects an image (JPG or PNG) of handwritten text and clicks **"Recognize Handwriting"**.
- JavaScript captures the form submission, sends the image to the `/upload` endpoint via a `POST` request using `fetch()`.

### 2. Flask Receives the Image (app.py)

- The `/upload` route in `app.py` receives the uploaded file.
- It validates the file type (only `.png`, `.jpg`, `.jpeg` are allowed).
- The image is saved to `static/uploads/` using a secure filename.

### 3. Image Preprocessing (preprocess.py)

The `preprocess_image()` function in `preprocess.py` enhances the image for better OCR accuracy:

| Step | Technique | Purpose |
|------|-----------|---------|
| 1 | **Load Image** | Read with OpenCV; fallback to Pillow if needed |
| 2 | **Resize** | Scale down images larger than 1000px for performance |
| 3 | **Grayscale** | Convert to single-channel for processing |
| 4 | **Histogram Equalization** | Improve contrast between text and background |
| 5 | **Gaussian Blur** | Reduce image noise |
| 6 | **Otsu Thresholding** | Convert to binary (black text on white background) |
| 7 | **Morphological Close** | Remove small noise artifacts and fill gaps |

### 4. Text Extraction (EasyOCR)

- EasyOCR's `readtext()` method runs a deep learning model on the image.
- It returns a list of detected text regions, each with bounding box coordinates, the recognized text, and a confidence score.
- The app sorts results **by Y-coordinate** (top to bottom) to reconstruct line order, then sorts words **by X-coordinate** (left to right) within each line.
- Words on the same line are grouped together using a Y-tolerance threshold.

### 5. Spelling Correction (TextBlob)

- The extracted text is passed to `TextBlob.correct()`, which uses a statistical model to fix common spelling errors introduced by OCR misreads.
- Both the raw extracted text and the corrected text are returned.

### 6. Response to Frontend (JSON)

The Flask backend returns a JSON response:

```json
{
  "success": true,
  "text": "Raw extracted text from OCR",
  "corrected": "Spelling-corrected version of the text",
  "original_image": "filename.jpg",
  "processed_image": "filename.jpg"
}
```

### 7. Frontend Displays Results

- JavaScript receives the JSON response and updates the page:
  - **Extracted Text** is displayed in a green alert box.
  - **Corrected Text** is displayed in a blue alert box.
  - The **original** and **processed** images are displayed for visual comparison.

---

## Key Technologies

| Component | Technology | Role |
|-----------|-----------|------|
| Web Framework | Flask | HTTP routing, template rendering, file handling |
| OCR Engine | EasyOCR | Deep learning-based handwriting text extraction |
| Image Processing | OpenCV + NumPy | Preprocessing pipeline to enhance image quality |
| Spelling Correction | TextBlob | Statistical spelling correction on OCR output |
| Frontend | HTML + Bootstrap 5 + JavaScript | User interface and async file upload |
