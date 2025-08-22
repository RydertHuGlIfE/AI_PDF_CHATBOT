# **Vortex Mind AI Adaptive E-Learning Platform**

This project is part of our vision to build an **AI-adapted e-learning platform**. This sophisticated web application allows users to upload a PDF, extract its content, interact with an AI for intelligent conversation, summarize documents in HTML format, and even generate code from the content. Utilizing cutting-edge AI models and seamless integration with Flask, this platform provides a high-performance, user-friendly interface for PDF interaction and document manipulation.

<pre> 📂 Project Structure 
  ├── static/ 
    │ └── styles/ 
          └── viewer.css 
          └── styles.css 
          └── favico.ico 
  └── templates/
      ├── index.html 
      └── viewer.html 
  └── main.py
  └── readme.md
  └── requirements.txt
</pre>

## **📌 Problem Statement**

Traditional e-learning platforms often provide static content that fails to adapt to individual learners.  
- Students spend hours going through **long PDFs and manuals** without personalized assistance.  
- Extracting **key insights, summaries, or relevant examples** requires significant effort.  
- Technical learners struggle to **convert concepts into executable code**.  
- Platforms rarely provide **contextual multimedia (like related videos)** to support different learning styles.  
- Annotation and adaptive learning feedback are limited.  

Hence, there is a need for an **AI-adapted E-learning platform** that makes study material interactive, dynamic, and learner-friendly.  

---

## **📊 Current Progress Status**

✅ Core features implemented:  
- PDF upload and text extraction.  
- AI-driven conversation based on PDF content.  
- Summarization into HTML format.  
- YouTube search integration.  
- Code generation from technical PDFs.  
- Light/Dark mode support.
- Mind Map creation.
- Quiz Generating 

🚧 Work still pending:  
- Better **UI improvements** for enhanced user experience.  

---

## **💡 Prototype Solution**

Our prototype addresses the problem by providing:  

1. **PDF Upload & Extraction** → Extracts text from PDFs instantly.  
2. **Conversational AI** → Users can chat with the AI about the PDF (e.g., “What’s on page 10?”).  
3. **AI Summarization** → Generates structured HTML summaries with topics, findings, and insights.  
4. **YouTube Integration** → Suggests related educational videos for deeper learning.  
5. **Annotation & Highlighting** → AI adds contextual notes directly within the PDF.  
6. **Code Generation** → Converts algorithms/equations from PDFs into **executable code**.  
7. **Theme Switching** → Light & Dark modes for accessibility and comfort.
8. **Mind Maps** → Create Mind Maps related to the PDF file uploaded.  
9. **Large Size** → It can take PDFs upto 50mb with 100+ pages.
10. **Quiz Creation** - Generate some of the most amazing quizes to test you knowledge

This is a **step toward an adaptive AI-powered e-learning platform** where documents become interactive and personalized to each learner’s needs.  

---

## **💡 Executing Instruction**
- You need to have a Google Gemini API key to run this program
- It is recommended to create a virtual Environment before running this to ensure better compatiblity [optional]
- To install All the necessary modules type :
- <pre> pip install -r requirements.txt </pre>
- Then if you are Inside Venv please install the modules INSIDE of the venv
- Run the program and visit 127.0.0.1/5000   (port number could be different but it is usually 5000)
- An OCR Scanned PDF is required, Handwritten OCR Scanned PDFs will not be recognised

---

## **🛠️ Tech Stack**

- **Python 3.x** – Backend language  
- **Flask** – Web framework  
- **PyPDF2** – PDF text extraction  
- **Google Gemini** – AI model integration  
- **HTML/CSS** – Frontend interface  

---

## **🎬 Prototype Screenshots**

### **1. Welcome Page & PDF Submission**  
Users upload PDFs, and the AI begins analyzing.  

<img width="1843" height="1118" alt="Screenshot From 2025-08-20 21-29-51" src="https://github.com/user-attachments/assets/27936adb-d883-4131-8aca-3aa6cc8463a9" />

### **2. PDF Uploaded & AI Ready for Interaction**  
AI is now active for queries based on the uploaded document.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/61885d15-2707-49e2-95b5-cc62ffe8bad2" />

### **3. Summarization Feature**  
Generates concise PDF summaries with key insights.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/46dd38c6-fd5a-4168-bf3a-b3ddbe6387eb" />

### **4. Mind-Map Feature**  
Generates a detailed mindmaps from the PDF.

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/8f632ad9-0cbc-4594-95c2-02d2f50155e0" />

### **5. YouTube Search Integration**  
Direct search for related videos from extracted topics.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/d33fe1fc-a65e-48f2-bd5f-48a847ad6a40" />

### **6. Quiz Generator**  
Direct search for related videos from extracted topics. 

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/eaccaf79-0385-4f08-a482-cf2271750918" />

### **7. Contextual Page Queries**  
Ask questions like *“What’s on page 10?”* for precise responses.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/36c8186d-3f92-4669-bb4f-6c466290a4e3" />

### **8. PDF Annotation Feature**  
Powerful annotations and contextual highlights.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/642e58bb-dd7e-4431-8641-864ead9801b8" />

### **9. AI-Generated Code from PDF**  
Transforms technical content into executable code.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/9416148e-10a5-438e-96f0-5eca8399514c" />

### **10. Light Mode Interface**  
Switch between dark and light themes for accessibility.  

<img width="1817" height="1099" alt="image" src="https://github.com/user-attachments/assets/29228941-be7a-4228-bd5a-79fd988b5d91" />

---

✨ With this prototype, we move a step closer to building a **truly AI-adapted e-learning platform**, where learning is **interactive, adaptive, and personalized**.  
