import os
from flask import Flask, render_template, request, jsonify
import easyocr
from preprocess import preprocess_image
from textblob import TextBlob
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

reader = easyocr.Reader(['en'], gpu=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        results = reader.readtext(filepath, detail=1)
        
        lines = []
        if results:
            results.sort(key=lambda r: r[0][0][1])
            
            current_line = [results[0]]
            y_tolerance = (results[0][0][2][1] - results[0][0][0][1]) * 0.7 
            
            for i in range(1, len(results)):

                prev_word_y = current_line[-1][0][0][1]
                current_word_y = results[i][0][0][1]
                
                if abs(current_word_y - prev_word_y) < y_tolerance:
                    current_line.append(results[i])
                else:
                    lines.append(current_line)
                    current_line = [results[i]]
            lines.append(current_line)

        sorted_lines = []
        for line in lines:
            line.sort(key=lambda r: r[0][0][0])
            sorted_lines.append(' '.join([res[1] for res in line]))
        
        extracted_text = '\n'.join(sorted_lines)
        
        corrected_text = str(TextBlob(extracted_text.replace('\n', ' ')).correct())
        
        return jsonify({
            'success': True,
            'text': extracted_text if extracted_text else 'No text detected.',
            'corrected': corrected_text,
            'original_image': filename,
            'processed_image': filename
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
