# AuralDine – AI-Based Indian Accent & Cuisine Recommender

AuralDine is an AI speech-analytics system that identifies a speaker’s Indian regional accent from English speech and recommends region-specific cuisine based on cultural roots. It integrates MFCC features, HuBERT embeddings, classical ML models, and deep learning classifiers.

## 🚀 Overview
AuralDine processes microphone/recorded speech, extracts HuBERT representations, predicts one of six Indian accents, and maps the accent to a curated cuisine list. The project demonstrates near-perfect adult accent recognition and includes analysis on word-level, sentence-level, and child-speech generalization.

## Project Report
[Project Report](https://github.com/Mer315/AuralDine/blob/main/Project_Report.pdf)

## 🎯 Features
- Indian accent detection (6-class)
- MFCC extraction & HuBERT embeddings
- Classical ML models (RF, SVM, KNN, etc.)
- Deep learning models (CNN-BN, Transformer)
- Word-level vs sentence-level comparison
- Adult → child domain shift analysis
- Cuisine recommendation web prototype

## 🧠 Model Summary

### Feature Extraction
- **MFCC (39-D)** for classical ML experiments  
- **HuBERT Base (13 layers × 768-D)** for SVMs, CNNs, Transformers

### Performance Highlights
- **MFCC + Random Forest:** 99.46% test accuracy  
- **HuBERT SVM:** ~99% (best at layers 2–3)  
- **CNN-BN (Final Model):** 99.94% validation accuracy  
- **Transformer:** ~99.56%  
- **Sentence-level:** 100%  
- **Word-level:** 99.6%  
- **Adult → Child:** Model confidence drops due to pitch & phoneme instability

## 🍽️ Cuisine Recommendation Logic
Accent → Region → Dishes

Examples:
- **Malayalam → Kerala:** Appam, Puttu, Avial  
- **Tamil → Tamil Nadu:** Dosa, Pongal, Chettinad Chicken  
- **Telugu → Andhra/Telangana:** Pesarattu, Gutti Vankaya, Hyderabadi Biryani  
- **Kannada → Karnataka:** Bisi Bele Bath, Neer Dosa  
- **Hindi (North) → North India:** Roti, Chole Bhature, Rajma Chawal  

## 🖥️ How It Works
1. Record/upload speech  
2. Extract HuBERT embeddings  
3. Predict accent via CNN-BN classifier  
4. Map accent → recommended cuisine  
5. Display accent + confidence + dishes in UI  

## 🛠️ Tech Stack
- Python, NumPy, Pandas  
- Librosa (audio processing)  
- PyTorch, Transformers (HuBERT)  
- scikit-learn  
- Matplotlib, Seaborn  
- Streamlit / Flask (prototype UI)

##🚀 How to Run the App

### 🖥️ Local Development

- 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at: [http://localhost:8000](http://localhost:8000)
- 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: [http://localhost:5173](http://localhost:3000)
---

### 🐳 Running with Docker

-  1. Build Containers
```bash
docker compose build
```
-  2. Start All Services
```bash
docker compose up
```
This starts:
* **Frontend** → [http://localhost:5173](http://localhost:3000)
* **Backend (FastAPI)** → [http://localhost:8000](http://localhost:8000)
* **ML Service** → [http://localhost:7000](http://localhost:7000)
- 🔄 Rebuild After Code Changes
```bash
docker compose down
docker compose up --build
```
---




## 📈 Key Insights
- HuBERT + CNN-BN outperforms MFCC baselines
- Sentence-level speech produces the most stable accent cues
- Early HuBERT layers capture accent strongly
- t-SNE shows clear accent clustering
- Child-speech generalization requires domain adaptation

## 🔮 Future Work
- Collect more real-world & child-speech samples  
- Add prosody features (pitch, rhythm, intonation)  
- End-to-end speech-to-cuisine model  
- Mobile deployment (Android/iOS)  
- Expand regional cuisine dataset  

## Screenshots
- ![WhatsApp Image 2025-11-30 at 21 26 09_6eca9987](https://github.com/user-attachments/assets/7caa2fb4-1f47-41d4-baad-c17d7c10c570)
- ![WhatsApp Image 2025-11-30 at 21 48 17_0268d118](https://github.com/user-attachments/assets/5b9265a6-3169-47e7-b6da-f663b999dd92)
- ![WhatsApp Image 2025-11-30 at 21 48 49_0615647d](https://github.com/user-attachments/assets/2e17e5c4-c898-40ff-aa5e-099e4cedc771)

## 👩‍💻 Authors
**V Sai Sumedha** (@mer315) - Model Training
**Yuvika Sai Simhadri** (@yuvikasai) - Frontend
**K Sri Karuna Reddy** (@srikarunareddy) - Backend
BVRIT Hyderabad College of Engineering for Women

## 📄 License
This project is released under the **MIT License**.

You are free to use, modify, distribute, and build upon this work, provided that the original authors are credited.

---
