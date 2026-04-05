# Skin Cancer Detection using Deep Learning

## 📌 Introduction
Skin cancer is one of the most common types of cancer worldwide. Early detection is crucial for effective treatment. This project uses deep learning techniques to classify different types of skin cancer from dermoscopic images.

---

## 🎯 Objective
To build a Convolutional Neural Network (CNN) model that can accurately classify skin lesion images into different categories.

---

## 📂 Dataset
- Dataset used: HAM10000 (Human Against Machine with 10000 training images)
- Source: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000

---

## 🛠️ Technologies Used
- Python
- TensorFlow / Keras
- NumPy
- Pandas
- OpenCV
- Matplotlib
- Scikit-learn

---

## 🧠 Model Architecture
- Convolutional Neural Network (CNN)
- Layers:
  - Conv2D
  - MaxPooling
  - Dropout
  - Dense Layers
- Activation Functions: ReLU, Softmax

---

## ⚙️ Project Workflow
1. Data Loading and Preprocessing
2. Image Resizing and Normalization
3. Model Building (CNN)
4. Model Training
5. Evaluation (Accuracy, Loss)
6. Prediction on New Images

---

## 📊 Results
- Achieved good accuracy on validation data
- Model is capable of identifying seven types of skin lesion



---

## ▶️ How to Run
1. Clone the repository:
   git clone https://github.com/your-username/skin-cancer-detection.git

2. Install dependencies:
   pip install -r requirements.txt

3. Run the notebook:
   Open skin_cancer_detection.ipynb in Jupyter or Google Colab

---

## 📁 Project Structure
skin-cancer-detection/
│
├── skin_cancer_detection.ipynb
├── requirements.txt
├── README.md
├── model.h5 (optional)
└── results/

---

## ⚠️ Note
- Dataset is not uploaded due to size limitations
- Download dataset from Kaggle link provided above

---

## 🚀 Future Improvements
- Improve model accuracy using advanced architectures (ResNet, EfficientNet)
- Deploy as a web application
- Add real-time prediction feature

---

## 👨‍💻 Author
Anupam kumar

---

## ⭐ Acknowledgements
- HAM10000 Dataset
- TensorFlow & Keras Documentation
