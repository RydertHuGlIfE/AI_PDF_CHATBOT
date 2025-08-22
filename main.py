from flask import Flask, render_template, request, send_file, session, redirect, url_for, jsonify
import os
import google.generativeai as genai
import PyPDF2
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import webbrowser
import json 

app = Flask(__name__)
script_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(script_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)


app.config['UPLOAD_FOLDER'] = uploads_dir
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'pdf'}

app.secret_key = "areterimkbsda"   

genai.configure(api_key="insert_api_key")
model = genai.GenerativeModel("models/gemini-1.5-flash", generation_config={
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 4000
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

if there is casual responses like hello or thank you in USER QUESTION: 
ignore PDF CONTENT and just respond accordingly for hi jsut respond like a normal chatbot

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


@app.route('/quiz/start', methods=['POST'])
def start_quiz():
    filename = session.get('pdf_filename', '')

    if not filename:
        return jsonify({"error": "No PDF Loaded"}), 400

    text_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".txt")
    if not os.path.exists(text_path):
        return jsonify({"error": "Extracted Text not found"}), 400

    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()

    prompt = f"""
    You are in quiz mode. Generate 5 MCQ questions with 4 options and correct answer,
    and 5 theoretical questions. Return **only JSON**, strictly in this format:
    {{
      "mcq": [
        {{"q": "question text", "options": ["A","B","C","D"], "answer": "B"}}
      ],
      "theory": [
        "theory question 1",
        "theory question 2"
      ]
    }}

    PDF CONTENT:
    {pdf_text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.candidates[0].content.parts[0].text.strip()

        # clean possible junk around JSON
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")  
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

        quiz_data = json.loads(raw_text)  # <-- safe parsing

        session['quiz'] = {
            "mcq": quiz_data["mcq"],
            "theory": quiz_data["theory"],
            "current_mcq": 0,
            "current_theory": 0,
            "phase": "mcq",
            "answers": []
        }
        session.modified = True

        first_q = quiz_data["mcq"][0]
        return jsonify({"question": first_q["q"], "options": first_q["options"]})

    except Exception as e:
        return jsonify({"error": f"Error generating Quiz: {str(e)}"}), 500



@app.route('/quiz/answer', methods=['POST'])
def quiz_answer():
    data = request.json
    user_answer = data.get("answer", "")

    quiz = session.get('quiz', None)
    if not quiz:
        return jsonify({"error": "Quiz not started"}), 400

    # --- MCQ MODE ---
    if quiz["phase"] == "mcq":
        q_index = quiz["current_mcq"]
        question = quiz["mcq"][q_index]["q"]
        correct = quiz["mcq"][q_index]["answer"]

        is_correct = user_answer.strip().lower() == correct.strip().lower()
        result = {
            "question": question,
            "your_answer": user_answer,
            "correct_answer": correct,
            "is_correct": is_correct
        }
        quiz["answers"].append(result)
        quiz["current_mcq"] += 1

        # if MCQs finished
        if quiz["current_mcq"] >= len(quiz["mcq"]):
            total = len(quiz["mcq"])
            correct_count = sum(1 for ans in quiz["answers"] if ans.get("is_correct"))
            score_msg = f"<h3>MCQ Round Completed!</h3><p>You scored <strong>{correct_count}/{total}</strong>.</p>"

            quiz["phase"] = "theory"
            session['quiz'] = quiz

            return jsonify({
                "result": result,
                "message": score_msg,
                "all_mcq_results": quiz["answers"],
                "next_question": quiz["theory"][0]
            })

        else:
            next_q = quiz["mcq"][quiz["current_mcq"]]
            session['quiz'] = quiz
            return jsonify({
                "result": result,
                "next_question": next_q["q"],
                "options": next_q["options"]
            })

    # --- THEORY MODE ---
    elif quiz["phase"] == "theory":
        q_index = quiz["current_theory"]
        question = quiz["theory"][q_index]

        eval_prompt = f"""
        Evaluate this theoretical answer:
        Question: {question}
        User Answer: {user_answer}

        Analyse on:
        - Coverage of topic
        - Depth of knowledge
        - Confidence Score (out of 10)
        - Marks out of 12

        Return clean bullet points only.
        """
        response = model.generate_content(eval_prompt)
        feedback = response.candidates[0].content.parts[0].text

        quiz["answers"].append({
            "question": question,
            "answer": user_answer,
            "evaluation": feedback
        })
        quiz["current_theory"] += 1

        # if more theory left
        if quiz["current_theory"] < len(quiz["theory"]):
            next_q = quiz["theory"][quiz["current_theory"]]
            session['quiz'] = quiz
            return jsonify({
                "feedback": feedback,
                "next_question": next_q
            })

        # if finished all theory
        else:
            mcq_results = [a for a in quiz["answers"] if "is_correct" in a]
            total_mcq = len(mcq_results)
            correct_mcq = sum(1 for a in mcq_results if a["is_correct"])
            score_msg = f"<h3>Quiz Completed!</h3><p>Your MCQ Score: <strong>{correct_mcq}/{total_mcq}</strong></p>"

            all_results = quiz["answers"]

            # EXIT QUIZ MODE
            session.pop('quiz', None)

            return jsonify({
                "feedback": feedback,
                "message": score_msg + "<p>You are now back to normal mode ✅</p>",
                "all_results": all_results
            })


@app.route("/mindmap", methods=['POST'])
def mindmap():
    filename = session.get('pdf_filename', '')
    
    if not filename:
        return jsonify({"error": "No PDF loaded"}), 400
    
    text_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + ".txt")
    if not os.path.exists(text_path):
        return jsonify({"error": "Extracted text not found"}), 400
    
    with open(text_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()
        
        prompt = f"""You are a highly sophisticated AI the text that I am going to be providing you, I need to study for some exam I need you to create the best mindmap the human history 
        has ever seen, anyone that lays eyes upon this piece should say I need this to study for my exam i dont need you to say alright sir ill do this and that you wil just say 
        Generating Mindmap: and use the pdf text that would be provided before that here are some ground html rules that U need to blindly follow unless you are stated to change
        everything from the pdf should be covered dont leave anything 
        IMPORTANT OUTPUT RULES:
        - Output valid HTML only (no Markdown, no backslashes) but dont mention html in the text and neither use ```.
        - Use <h3> for section titles.
        - Use <ol><li> for numbered lists.
        - Use <strong> for bold.
        - Use <p> for paragraphs.
        - Do not include <script> or event handlers.
        - use "  " this spacing for the bullet points and = this for subpoints
        - dont use ``` html tags
        here is the pdf text create the mindmap in try bullet points or otherwise feel suitable..
        {pdf_text}"""
        
        try:
            response = model.generate_content(prompt)
            ai_res = "".join([p.text for p in response.candidates[0].content.parts])
            return jsonify({"response":  ai_res, "is_html": True})
        except Exception as e:
            return jsonify({"error": f"Error Generating the mind map {str(e)}"}), 500
    

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



