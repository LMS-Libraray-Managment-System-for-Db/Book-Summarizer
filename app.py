from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from extract_pdf import extract_text_from_pdf
from model import query, allowed_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """Handle file upload and return the summary of the PDF content."""
    if 'pdf-file' not in request.files:
        return jsonify({"error": "No PDF file part"}), 400
    file = request.files['pdf-file']
    if file.filename == '':
        return jsonify({"error": "No PDF file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text = extract_text_from_pdf(file_path)
        summary = query(extracted_text)
        os.remove(file_path)  # Remove the uploaded file
        return jsonify({"summary": summary})
    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
