from flask import Flask, render_template, request, send_file, session, redirect, url_for, jsonify
import os
import google.generativeai as genai
import PyPDF2
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import webbrowser

app = Flask(__name__)
script_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(script_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)


app.config['UPLOAD_FOLDER'] = uploads_dir
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf'}

app.secret_key = "areterimkbsda"   

genai.configure(api_key="Enter Your API Key here...")
model = genai.GenerativeModel("models/gemini-1.5-flash", generation_config={
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1000
})


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/viewer')
def viewer():
    if 'pdf_filename' not in session:
        return redirect(url_for('index'))
    return render_template("viewer.html")


@app.route('/get-pdf-info')
def get_pdf_info():
    filename = session.get('pdf_filename')
    if not filename:
        return jsonify({"error": "No PDF loaded"}), 400
    return jsonify({"filename": filename})


@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({"error": "No file selected"}), 400
        
        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        extracted_text = extract_text_from_pdf(filepath)
        if extracted_text.startswith("Error reading PDF"):
            return jsonify({"error": extracted_text}), 400
        
        text_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        
        session['pdf_filename'] = filename
        
        return jsonify({
            "success": True,
            "filename": filename,
            "message": "PDF uploaded successfully",
            "text_length": len(extracted_text)
        })
        
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500


@app.route('/pdf/<filename>')
def serve_pdf(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    filename = session.get('pdf_filename', '')

    if not filename:
        return jsonify({"error": "No PDF loaded"}), 400
    
    text_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".txt")
    if not os.path.exists(text_path):
        return jsonify({"error": "Extracted text not found"}), 400
    
    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()

    prompt = f"""
You are a helpful assistant.

IMPORTANT OUTPUT RULES:
- Output valid HTML only (no Markdown, no backslashes) but dont mention html in the text and neither use ```.
- Use <h3> for section titles.
- Use <ol><li> for numbered lists.
- Use <strong> for bold.
- Use <p> for paragraphs.
- Do not include <script> or event handlers.
- use "  " this spacing for the bullet points and = this for subpoints
While Making bullet points give a space after heading eg 
try to give most answers in bullet points unless asked...
try to be as consice and give a short answer as well unless asked in detail 
and dont use ``` or html words in the response and make it look clean
instead of numbers use bullet points

topic 
   1: h1
   2: h2 

PDF CONTENT:
{pdf_text}

USER QUESTION:
{user_message}
"""

    if user_message.startswith("search youtube for:"):
        topic = user_message.replace("search youtube for:", "").strip()
        search_url = f"https://www.youtube.com/results?search_query={topic.replace(' ', '+')}"
        webbrowser.open(search_url)
        return jsonify({"response": f"<p>Opened YouTube search for <strong>{topic}</strong> in your browser! 🎥</p>", "is_html": True})

    try:
        response = model.generate_content(prompt)
        ai_response = "".join([p.text for p in response.candidates[0].content.parts])
        return jsonify({"response": ai_response, "is_html": True})
    except Exception as e:
        return jsonify({"error": f"Error generating response: {str(e)}"}), 500


@app.route('/summarize', methods=['POST'])
def summarize():
    filename = session.get('pdf_filename', '')

    if not filename:
        return jsonify({"error": "No PDF loaded"}), 400
    
    text_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".txt")
    if not os.path.exists(text_path):
        return jsonify({"error": "Extracted text not found"}), 400
    
    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()

    prompt = f"""
You are a helpful assistant. Provide an HTML-only summary of the following PDF.

STRUCTURE:
<h3>1. Main topics and key points</h3>
<ol><li>...</li></ol>

<h3>2. Important findings or conclusions</h3>
<ol><li>...</li></ol>

<h3>3. Significant data or statistics</h3>
<ol><li>...</li></ol>

<h3>4. Overall theme and purpose</h3>
<p>...</p>


try to give most answers in bullet points unless asked...
try to be as consice and give a short answer as well unless asked in detail 
and dont use ``` or html words in the response and make it look clean
instead of numbers use bullet pts

PDF CONTENT:
{pdf_text}
"""

    try:
        response = model.generate_content(prompt)
        ai_response = "".join([p.text for p in response.candidates[0].content.parts])
        return jsonify({"response": ai_response, "is_html": True})
    except Exception as e:
        return jsonify({"error": f"Error generating summary: {str(e)}"}), 500


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file with improved error handling"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if pdf_reader.is_encrypted:
                try:
                    pdf_reader.decrypt("")  
                except:
                    return "Error reading PDF: Document is password protected"
            
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                return "Error reading PDF: No pages found in document"
            
            text = ""
            for i, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    text += page_text + "\n"
                except Exception:
                    continue
            
            extracted_text = text.strip()
            if not extracted_text:
                return "Error reading PDF: No text could be extracted. Might be scanned/images only."
            return extracted_text
            
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({"error": "File too large. Maximum size is 50MB."}), 413


@app.errorhandler(413)
def handle_413(e):
    return jsonify({"error": "File too large. Maximum size is 50MB."}), 413


if __name__ == '__main__':
    app.run(debug=True)

