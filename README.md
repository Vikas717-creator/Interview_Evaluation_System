# AI Powered Interview Evaluation System

An AI-based interview practice and evaluation platform built with **Streamlit**, **Sentence Transformers**, and **Speech Recognition**.  
The system evaluates user answers using **semantic similarity** instead of exact matching and provides performance analytics through an interactive dashboard.

---

## 🚀 Features

- AI-based answer evaluation using **Sentence Transformers**
- Supports **text input and voice input**
- Randomized interview questions
- Multi-subject interview support
- Automatic scoring system
- Performance tracking dashboard
- Attempt history and analytics
- Score distribution visualization
- Subject-wise performance analysis

---

## 🧠 How the System Works

1. User enters personal details.
2. Selects interview subject.
3. System loads random questions.
4. User answers via **text or voice**.
5. AI evaluates the answer using **semantic similarity**.
6. Score is generated.
7. Results are stored.
8. Dashboard shows performance analytics.

---

## 🏗 System Architecture
User
│
▼
Streamlit Interface
│
├── Text Input
├── Voice Input (Speech Recognition)
│
▼
Answer Evaluation Engine
(Sentence Transformers + Cosine Similarity)
│
▼
Scoring System
│
▼
Results Storage (CSV)
│
▼
Performance Dashboard (Plotly)


## 📂 Project Structure


AI-Interview-System
│
├── app.py
├── evaluator.py
├── question_loader.py
├── voice_input.py
│
├── python_questions.json
├── java_questions.json
├── datascience_questions.json
│
├── results.csv
├── requirements.txt
└── README.md

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ai-interview-system.git
cd ai-interview-system

Install dependencies
pip install -r requirements.txt


▶️ Run the Application

Start the Streamlit server
streamlit run app.py


📊 Dashboard Features

The dashboard provides:
Total interview attempts
Average score
Best and lowest scores
Score trend over time
Score distribution
Subject-wise performance
Attempt history

🧪 Technologies Used

Python
Streamlit
Sentence Transformers
Scikit-learn