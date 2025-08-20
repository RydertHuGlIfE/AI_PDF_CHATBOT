# **🔥 The Ultimate PDF Chat & AI Summarizer 🔥**

This sophisticated web application allows users to upload a PDF, extract its content, interact with an AI for intelligent conversation, summarize documents in HTML format, and even generate code from the content. Utilizing cutting-edge AI models and seamless integration with Flask, this platform provides a high-performance, user-friendly interface for PDF interaction and document manipulation.

/AI_PDF_CHATBOT
│
├── static
│   ├── styles
│   │   └── viewer.css
│
└── templates
    ├── index.html
    └── viewer.html



## **💻 Features:**

- **PDF Upload & Extraction**: Upload your PDF files, and the app extracts the text for analysis and interaction.
- **Conversational AI**: Engage with an AI capable of answering your questions based on the uploaded PDF content.
- **PDF Summarization**: Summarize lengthy PDFs into concise HTML-based summaries with key topics, findings, and conclusions.
- **YouTube Search Integration**: Directly search YouTube for related content by providing topics from the PDF.
- **PDF Annotation**: Annotate the document while receiving contextual highlights and comments from the AI.
- **Code Generation**: Convert technical content from PDFs into executable code, powered by AI.
- **Light & Dark Mode**: Toggle between light and dark modes based on your visual preferences.


## **🎬 Demo Screenshots**

The following section illustrates key actions within the application with screenshots:


**Screenshot 1: Welcome Page & PDF Submission**  
This is the **intro page** where users can submit their PDF files for processing. Upon upload, the AI begins analyzing the document.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/83daabbe-42ac-4d3a-a0b5-29adb0bec359" />

**Screenshot 2: PDF Uploaded & AI Ready for Interaction**  
After successful upload, the AI becomes active, prepared to engage in any PDF-related queries. The interface updates to reflect this dynamic interaction.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/07422af4-9ec7-45e1-81ff-1ec511692c6a" />

**Screenshot 3: Summarization Feature**  
By clicking on the **Summarize** button, the AI generates an HTML-based summary of the entire PDF, extracting main topics and key insights.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/ea5b74f3-a489-42a6-b1bd-64329804b83d" />


**Screenshot 4: YouTube Search Integration**  
Clicking on the **YouTube** button triggers a direct search for related video content, leveraging the extracted topic for precision.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/7a2d2272-a5a4-49f8-b128-ab080385f140" />


**Screenshot 5: Successful Operation**  
The functionality works as expected—AI delivers intelligent responses, demonstrating the platform's ability to process and analyze PDF content seamlessly.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/3bfbd5e0-e774-4a0f-ac87-988b23811f9c" />


**Screenshot 6: Contextual Response to Page Queries**  
Users can query the AI for specific page-based information (e.g., "What’s on page 10?"). The AI retrieves relevant content with precision, responding appropriately.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/56e1544a-6c8d-4c55-a06c-fa97854a6f75" />


**Screenshot 7: PDF Annotation Feature**  
While interacting with the AI, users can **annotate** the document. The AI highlights key sections and provides additional context or insights directly within the PDF.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/4b43be24-f86e-4888-ac52-7a3da92ce2f0" />


**Screenshot 8: AI-Generated Code from PDF**  
The AI is capable of transforming the technical content from the PDF into executable **code**. Ask the AI for code generation, and it delivers a working solution.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/3a11fd7c-d68a-4157-9126-8680bedb1b6a" />


**Screenshot 9: Expanded Code Example**  
Further demonstrating the AI’s capability, the app displays additional code generated from the PDF, illustrating the AI's ability to handle more extensive document-based programming tasks.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/224ccde1-4603-4a86-8e42-b08794effc9e" />


**Screenshot 10: Light Mode Interface**  
For a modern, clean aesthetic, users can switch to **light mode**, enhancing the overall user experience during daytime usage.

<img width="1600" height="968" alt="image" src="https://github.com/user-attachments/assets/f5888651-6f71-43b0-bfee-edc37610a901" />


## **💡 How It Works**

### **1. Upload Your PDF**
Upload your PDF file, and the system will extract the text using **PyPDF2** for further processing.

### **2. AI-Driven Conversation**
Once the text is extracted, the **Google Gemini 1.5** AI model interprets the content, allowing users to engage in natural language queries about the document.

### **3. Summarize Your Document**
The AI analyzes the document and provides a concise summary in **HTML** format, organized by key sections like topics, findings, and data.

### **4. YouTube Search Integration**
If more information is required, the AI integrates with YouTube to search for relevant video content related to the PDF.

### **5. Annotate & Highlight PDF Content**
As users interact with the AI, they can **annotate** and highlight sections of the PDF. This creates a dynamic, interactive document review experience.

### **6. Code Generation**
For technical documents, the AI can generate **working code** based on the content, parsing algorithms, equations, and other programming-related information.

### **7. Switch Between Themes**
Toggle between **light mode** for a clean, bright interface or **dark mode** for those who prefer a more subdued and eye-friendly design.

---

## **⚙️ Prerequisites**

- **Python 3.x**
- **Flask** (Web Framework)
- **PyPDF2** (PDF Text Extraction)
- **Google Gemini** (AI Model Integration)
- **Werkzeug** (File Handling)

---


