# 🌾 Smart Paddy AI
### Rice Disease Detection & Agricultural Decision Support System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**Smart Paddy AI** is a deep learning-based web application for detecting rice leaf diseases and providing agricultural decision support. Built using **EfficientNetB0 Transfer Learning**, it achieves **85%+ validation accuracy** across 10 disease classes.

---

## 🚀 Live Demo

👉 [Click here to try the app](https://huggingface.co/spaces/dharshini26042005/smart-paddy-ai)

---

## 🔬 Features

| Feature | Description |
|---------|-------------|
| 🧠 **Disease Detection** | Detects 10 rice diseases using EfficientNetB0 |
| 🔥 **Grad-CAM** | Visual explainability heatmaps for infected regions |
| 📊 **Severity Estimation** | Estimates disease severity (Mild / Moderate / Severe) |
| 🌿 **Crop Health Index** | 0-100 health score for the crop |
| 📋 **PDF Report** | Downloadable diagnostic report |
| 🌐 **Bilingual** | English & Tamil language support |
| 🔊 **Voice Output** | Text-to-speech in Tamil & English |
| 📈 **Analytics Dashboard** | Scan history and disease trends |
| 📐 **Research Metrics** | Confusion matrix, ROC curves, classification report |

---

## 🦠 Disease Classes

```
1. Bacterial Leaf Blight
2. Bacterial Leaf Streak  
3. Bacterial Panicle Blight
4. Blast
5. Brown Spot
6. Dead Heart
7. Downy Mildew
8. Hispa
9. Normal (Healthy)
10. Tungro
```

---

## 🏗️ Model Architecture

```
EfficientNetB0 (ImageNet pretrained)
    ↓
GlobalAveragePooling2D
    ↓
BatchNormalization
    ↓
Dense(256, ReLU) → Dropout(0.4)
    ↓
Dense(128, ReLU) → Dropout(0.3)
    ↓
Dense(10, Softmax)
```

**Training Strategy:**
- Phase 1: Head training (backbone frozen) — 20 epochs
- Phase 2: Fine-tuning top 30 layers — 40 epochs
- Optimizer: Adam (lr=1e-3 → 1e-5)
- Loss: Categorical Cross-Entropy + Label Smoothing
- Augmentation: Rotation, Flip, Zoom, Brightness, Shear

---

## 📁 Project Structure

```
smart_paddy_ai/
├── app.py                  ← Main Streamlit application
├── train.py                ← Model training pipeline
├── requirements.txt        ← Dependencies
├── model/
│   ├── paddy_model.h5      ← Trained model
│   └── class_indices.json  ← Class mapping
└── utils/
    ├── predict.py          ← Inference engine
    ├── severity.py         ← Severity estimation
    ├── gradcam.py          ← Grad-CAM explainability
    ├── advisory.py         ← Agricultural advisory
    ├── ai_expert.py        ← AI chatbot
    ├── chatbot.py          ← Rule-based responses
    ├── logger.py           ← Event logging (SQLite)
    ├── pdf_report.py       ← PDF report generator
    ├── evaluation.py       ← Model evaluation metrics
    ├── voice.py            ← Text-to-speech
    └── sanity_check.py     ← Post-prediction validator
```

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/dharshini26042005/smart-paddy-ai.git
cd smart-paddy-ai

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Validation Accuracy | 85%+ |
| Model Size | 33 MB |
| Input Size | 128×128×3 |
| Inference Time | <1 second |

---

## 🛠️ Tech Stack

- **Deep Learning:** TensorFlow 2.15, Keras, EfficientNetB0
- **Explainability:** Grad-CAM
- **Frontend:** Streamlit
- **Visualization:** Plotly, Matplotlib, Seaborn
- **PDF Generation:** ReportLab
- **TTS:** gTTS
- **Database:** SQLite
- **Deployment:** Hugging Face Spaces

---

## 👩‍💻 Author

**Dharshini** — PG Research Project
Auxilium College

---

## 📄 License

This project is licensed under the MIT License.
