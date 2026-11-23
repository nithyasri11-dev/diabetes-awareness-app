# 💙 Diabetes Awareness
### An Explainable Machine Learning-Based Health Assessment and Awareness Platform

## 📌 Project Overview

Diabetes Awareness is an interactive HealthTech web application developed using Python and Streamlit. The project combines Machine Learning, Explainable Artificial Intelligence (XAI), Predictive Analytics and health education to make diabetes-related health information easier to understand.

The application allows users to enter health and lifestyle information, explore machine-learning model outputs, understand feature importance, interact with an educational chatbot and maintain their assessment history.

The primary objective is to provide an accessible health-awareness platform that combines technical intelligence with educational support.

**Note:** This project is an educational prototype and is not a medical diagnostic system.

## 🎯 Objectives

- Develop an interactive diabetes health-awareness platform.
- Integrate a trained machine-learning classification model.
- Improve model interpretability using Explainable AI.
- Visualise machine-learning performance metrics.
- Provide bilingual health education in English and Tamil.
- Encourage healthy habits through interactive quizzes and challenges.
- Maintain individual assessment records.

## ✨ Key Features

### 1. Machine Learning-Based Health Assessment
Collects demographic, lifestyle and health-related information and generates a model classification and positive-class score when supported by the model.

### 2. Explainable AI
Uses Permutation Feature Importance to identify which features influence the model's overall performance.

### 3. Predictive Analytics
Displays model evaluation metrics such as:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

### 4. Bilingual Health Chatbot
Provides general diabetes-awareness information in English and Tamil.

### 5. Diabetes Prevention Quest
Includes interactive health quizzes, daily wellness challenges, points and achievements.

### 6. Personal Assessment History
Allows users to view their previously saved health assessment records.

### 7. Health Report
Provides a record-management foundation for reviewing assessment information. PDF reporting can be enabled when the PDF-generation implementation is included in the deployed application.

### 8. Dark Mode Interface
Provides a dark-themed interface with a navy background, teal highlights and readable text.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| Scikit-learn | Machine learning and feature importance |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Joblib | Model loading |
| Plotly | Interactive visualisations |
| ReportLab | PDF generation support in the updated implementation |
| GitHub | Version control and project hosting |

## 📊 Dataset

The project uses the CDC Diabetes Health Indicators dataset distributed through the UCI Machine Learning Repository.

The dataset contains health and lifestyle indicators associated with diabetes-related status.

Some of the features used in the application include:

- Age
- BMI
- High blood pressure history
- High cholesterol history
- Smoking history
- Physical activity
- Fruit consumption
- Vegetable consumption
- General health
- Physical health

The model produces Class 0 or Class 1 outputs. These do not distinguish Type 1 from Type 2 diabetes.

## 🧠 Explainable AI Methodology

The application uses Permutation Feature Importance.

This method evaluates the change in model performance when the values of an individual feature are randomly shuffled.

Features that cause a greater reduction in performance when shuffled may be more important to the model's predictions.

The application presents feature-importance comparisons and visualisations to improve understanding of model behaviour.

These explanations do not establish causation or represent individual medical risk.

## ⚙️ Installation and Execution

### Prerequisites

- Python 3.10 or compatible version
- Visual Studio Code
- Git
- Required project files and trained model artifacts

### Step 1: Clone the Repository

```bash
git clone https://github.com/nithyasri11-dev/diabetes-awareness-app.git
```

### Step 2: Navigate to the Project Folder

```bash
cd diabetes-awareness-app
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 📁 Project Structure

```text
diabetes-awareness-app/
│
├── app.py
├── requirements.txt
├── download_uci.py
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── diabetes_health_indicators.csv
│
├── models/
│   ├── diabetes_model.joblib
│   ├── feature_names.joblib
│   └── model_comparison.csv
│
├── modules/
│
└── user_records/
```

The actual contents of the data, models and modules folders depend on the files included in the repository.

## 🔒 Limitations and Responsible Use

- The application is intended for educational awareness.
- Model outputs are not medical diagnoses.
- Class 0 and Class 1 do not represent Type 1 and Type 2 diabetes.
- The displayed model score is not necessarily a calibrated probability of future diabetes.
- The source dataset is based on US survey information and may not generalise to other populations.
- Health assessment records should be protected using appropriate security and persistent-storage mechanisms.

Users should consult qualified healthcare professionals for medical screening and advice.

## 🚀 Future Enhancements

- Integration of SHAP for individual prediction explanations.
- Improved model validation and calibration.
- Secure database integration.
- Enhanced Tamil chatbot capabilities.
- More comprehensive PDF reporting.
- Improved assessment-history visualisations.
- User experience testing and evaluation.

## 👩‍💻 Project Repository

**GitHub:**  
https://github.com/nithyasri11-dev/diabetes-awareness-app

---

*Developed as a HealthTech educational project focused on diabetes awareness, explainable machine learning and interactive health education.*