# 🌱 Crop Health Monitoring System using UAV
A machine learning–powered system for real-time agricultural health analysis using UAV (drone) imagery. The project detects crop stress, disease patterns, and vegetation health to enable timely farm interventions and improve agricultural productivity.


# Features

UAV-based imagery capture for high-resolution farm monitoring

Image processing pipeline to extract vegetation indices (NDVI, GNDVI)

Machine learning models for disease detection and stress classification

Real-time inference for early detection of crop issues

Optimized segmentation for precise health zone identification


# 🛠️ Tech Stack

Languages: Python

Libraries & Frameworks: OpenCV, NumPy, Scikit-learn, TensorFlow / PyTorch, Matplotlib

Tools: Jupyter Notebook, Git/GitHub

Data Source: UAV/drone imagery


# 📂 Project Structure
📦 Crop-Health-Monitoring-System-Using-UAV
 ┣ 📂 data/                # Sample UAV images
 ┣ 📂 notebooks/           # Jupyter notebooks for model training & testing
 ┣ 📂 src/                 # Source code (image processing, ML pipeline)
 ┣ 📜 requirements.txt     # Dependencies
 ┣ 📜 README.md            # Project documentation
 ┗ 📜 LICENSE              # License file

 # ⚙️ Installation & Setup

Clone the repository

git clone https://github.com/<your-username>/Crop-Health-Monitoring-System-Using-UAV.git
cd Crop-Health-Monitoring-System-Using-UAV


# Install dependencies

pip install -r requirements.txt


Run the notebook or script

jupyter notebook notebooks/crop_health_analysis.ipynb

# 🚀 How It Works

Image Acquisition: UAV drones capture high-resolution farm images.

Preprocessing: Images undergo resizing, noise removal, and vegetation index extraction.

Segmentation: Identifies healthy and stressed zones using image processing.

Classification: ML/DL models classify crop health status.

Output: Generates a visual health map with actionable insights.

# 📊 Results

High segmentation accuracy for vegetation mapping

Early detection of crop stress before visual symptoms appear

Optimized processing pipeline for faster inference

# 📜 Future Improvements

Integrate IoT sensors for real-time environmental data

Build a mobile/web dashboard for farmers

Expand dataset to multiple crop types and regions
